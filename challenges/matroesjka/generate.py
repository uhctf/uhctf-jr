"""Een zip-bestand achter een afbeelding geplakt: de foto opent gewoon, maar als zip zit er een geheim in."""
import hashlib
import io
import random
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.units import cm

from jr.pdf import MARGE, Pdf, begeleider

TEKST = {
    "nl": {
        "titel": "Matroesjka",
        "intro": "Een hacker heeft een geheim verstopt. We vonden alleen deze vakantiefoto op de gedeelde map. "
                 "Volgens onze speurders zit er meer in de foto dan je op het eerste zicht ziet.",
        "opdracht": "Open {bestand} op de laptop. Ziet het eruit als een gewone foto? Kijk ook naar hoe groot het bestand is, "
                    "en probeer het eens met een ander programma te openen.",
        "groet": "Groeten uit zee!",
        "dieper": "Bijna! Kijk nog dieper...",
        "geheim": "Gevonden! Het antwoord is: {antwoord}\n",
        "oplossing": [
            "Achter de afbeelding zit een zip-bestand geplakt. Een fotoviewer leest enkel het begin en stopt aan het einde van de afbeelding. "
            "Een zip-programma zoekt de inhoudstafel aan het einde van het bestand en vindt zo het verstopte bestand.",
            "Windows: kopieer het bestand naar het bureaublad, hernoem {bestand} naar .zip (bestandsextensies moeten zichtbaar zijn) "
            "en open het. Of: rechtsklik > 7-Zip > Archief openen.",
            "macOS of Linux: unzip {bestand}. Oudere deelnemers kunnen ook file of binwalk gebruiken.",
        ],
        "lagen": "Er zijn {n} lagen: elke zip bevat weer een foto met een zip erachter. In de laatste zit {geheim}.",
        "grootte": "Bestandsgrootte: {totaal} bytes, waarvan {foto} bytes foto. SHA-256: {hash}",
        "controle": "Controleer na het kopiëren naar de laptops of de netwerkshare dat grootte en SHA-256 nog kloppen.",
        "hints": ["Een bestand kan meer bevatten dan wat je programma toont. Hoe groot is deze foto?",
                  "Wat als het geen foto was, maar een ander soort bestand? Probeer de extensie te veranderen.",
                  "Hernoem het bestand naar .zip (of open het met 7-Zip) en kijk wat erin zit."],
    },
    "en": {
        "titel": "Matryoshka",
        "intro": "A hacker hid a secret. All we found was this holiday photo on the shared folder. "
                 "Our investigators say there is more in this photo than meets the eye.",
        "opdracht": "Open {bestand} on the laptop. Does it look like a normal photo? Also look at how big the file is, "
                    "and try opening it with another program.",
        "groet": "Greetings from the sea!",
        "dieper": "Almost! Look even deeper...",
        "geheim": "Found it! The answer is: {antwoord}\n",
        "oplossing": [
            "A zip file is glued behind the image. A photo viewer only reads the start and stops at the end of the image. "
            "A zip program looks for the table of contents at the end of the file and so finds the hidden file.",
            "Windows: copy the file to the desktop, rename {bestand} to .zip (file extensions must be visible) "
            "and open it. Or: right-click > 7-Zip > Open archive.",
            "macOS or Linux: unzip {bestand}. Older participants can also use file or binwalk.",
        ],
        "lagen": "There are {n} layers: each zip contains another photo with a zip behind it. The last one holds {geheim}.",
        "grootte": "File size: {totaal} bytes, of which {foto} bytes photo. SHA-256: {hash}",
        "controle": "After copying to the laptops or the network share, check that size and SHA-256 still match.",
        "hints": ["A file can contain more than what your program shows. How big is this photo?",
                  "What if it was not a photo, but another kind of file? Try changing the extension.",
                  "Rename the file to .zip (or open it with 7-Zip) and look inside."],
    },
}
GEHEIM = "geheim.txt"


def foto(tekst: str, rng: random.Random) -> bytes:
    """Eenvoudige 'vakantiefoto': lucht, zon, zee en een tekst."""
    b, h = 800, 500
    im = Image.new("RGB", (b, h))
    d = ImageDraw.Draw(im)
    lucht = (rng.randint(80, 140), rng.randint(160, 210), 255)
    for y in range(h // 2 + 40):
        f = y / (h / 2)
        d.line([(0, y), (b, y)], fill=tuple(int(c + (255 - c) * f * 0.6) for c in lucht))
    zx, zy = rng.randint(100, b - 100), rng.randint(60, 140)
    d.ellipse([zx - 50, zy - 50, zx + 50, zy + 50], fill=(255, 210, 60))
    d.rectangle([0, h // 2 + 40, b, h], fill=(30, rng.randint(90, 130), 190))
    for _ in range(25):  # golfjes
        x, y = rng.randint(0, b), rng.randint(h // 2 + 60, h - 20)
        d.arc([x - 30, y - 8, x + 30, y + 8], 200, 340, fill=(220, 240, 255), width=3)
    d.polygon([(0, h), (0, h - 70), (b, h - 30), (b, h)], fill=(240, 215, 150))  # strand
    d.text((b / 2, h - 35), tekst, fill=(60, 40, 20), font=ImageFont.load_default(size=36), anchor="mm")
    uit = io.BytesIO()
    im.save(uit, "PNG")
    return uit.getvalue()


def plak_zip(afbeelding: bytes, bestanden: dict[str, bytes]) -> bytes:
    """Plak een zip achter de afbeelding. Python schrijft de offsets vanaf het begin van het hele bestand,
    zodat ook strenge zip-programma's (zoals de ingebouwde van Windows) het archief vinden."""
    buf = io.BytesIO(afbeelding)
    buf.seek(0, 2)
    with zipfile.ZipFile(buf, "a", compression=zipfile.ZIP_DEFLATED) as z:
        for naam, data in bestanden.items():
            # vaste datum: elke bouw geeft hetzelfde bestand (en dezelfde SHA-256)
            z.writestr(zipfile.ZipInfo(naam, date_time=(2025, 7, 14, 12, 0, 0)), data, zipfile.ZIP_DEFLATED)
    return buf.getvalue()


def maak(params: dict) -> tuple[bytes, int]:
    """Geeft het bestand en de grootte van de buitenste foto terug."""
    t = TEKST.get(params["taal"], TEKST["nl"])
    if params["lagen"] < 1:
        raise ValueError("lagen moet minstens 1 zijn")
    rng = random.Random(params["seed"])
    naam = params["bestandsnaam"]
    stam, ext = (naam.rsplit(".", 1) + ["png"])[:2]
    inhoud = {GEHEIM: t["geheim"].format(antwoord=params["antwoord"]).encode()}
    # van binnen naar buiten: elke laag is een foto met de vorige laag als zip erachter
    for laag in range(params["lagen"], 0, -1):
        afbeelding = foto(t["groet"] if laag == 1 else t["dieper"], rng)
        bestand = plak_zip(afbeelding, inhoud)
        inhoud = {f"{stam}-{laag}.{ext}": bestand}
    return bestand, len(afbeelding)


def pak_uit(bestand: bytes) -> str:
    """Pak laag na laag uit tot geheim.txt, zoals een deelnemer dat doet."""
    while True:
        with zipfile.ZipFile(io.BytesIO(bestand)) as z:
            namen = z.namelist()
            if GEHEIM in namen:
                return z.read(GEHEIM).decode()
            bestand = z.read(namen[0])
        Image.open(io.BytesIO(bestand)).verify()


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, naam = params["antwoord"], params["bestandsnaam"]
    bestand, fotogrootte = maak(params)
    (uit / naam).write_bytes(bestand)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    p.regel(t["opdracht"].format(bestand=naam))
    breedte = 12 * cm
    p.ruimte(breedte * 5 / 8)
    p.c.drawImage(str(uit / naam), MARGE, p.y, breedte, breedte * 5 / 8)
    p.opslaan()

    oplossing = [r.format(bestand=naam) for r in t["oplossing"]]
    if params["lagen"] > 1:
        oplossing.append(t["lagen"].format(n=params["lagen"], geheim=GEHEIM))
    oplossing += [t["grootte"].format(totaal=len(bestand), foto=fotogrootte, hash=hashlib.sha256(bestand).hexdigest()),
                  t["controle"]]
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, oplossing, t["hints"], params["taal"])
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    bestand, _ = maak(params)
    Image.open(io.BytesIO(bestand)).verify()
    verwacht = TEKST.get(params["taal"], TEKST["nl"])["geheim"].format(antwoord=params["antwoord"])
    assert pak_uit(bestand) == verwacht
    # ook met echte zip-programma's, als ze er zijn: geen waarschuwingen over extra bytes voor het archief
    with tempfile.TemporaryDirectory() as tmp:
        pad = Path(tmp) / params["bestandsnaam"]
        pad.write_bytes(bestand)
        if shutil.which("unzip"):
            r = subprocess.run(["unzip", "-t", str(pad)], capture_output=True, text=True)
            assert r.returncode == 0, f"unzip: {r.stdout}{r.stderr}"
        if shutil.which("7z"):
            r = subprocess.run(["7z", "t", str(pad)], capture_output=True, text=True)
            assert r.returncode == 0 and "Warnings" not in r.stdout, f"7z: {r.stdout}{r.stderr}"
