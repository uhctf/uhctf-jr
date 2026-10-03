"""QR-code in donkerblauw op zwart: onzichtbaar tot je de afbeelding bewerkt met de x-ray tool."""
import shutil
import subprocess
import tempfile
from pathlib import Path

import segno
from reportlab.lib.units import cm

from jr.pdf import MARGE, Pdf, begeleider
from jr.shared import gebruik

TEKST = {
    "nl": {
        "titel": "Robot-QR",
        "intro": "Afbeeldingen kunnen meer bevatten dan op het eerste zicht lijkt. Deze robot draagt een geheim op zijn borst, "
                 "maar je ogen zien het nauwelijks.",
        "opdracht": "Open beeldbewerker/index.html op de computer: de afbeelding staat al klaar. Bewerk ze tot je iets herkent. "
                    "Scan het resultaat met je telefoon en schrijf het antwoord op.",
        "oplossing": "De QR-code is donkerblauw op zwart. Verhoog helderheid en contrast, of zet het blauwe kanaal hoog en de andere "
                     "kanalen laag, tot het patroon scherp zichtbaar is. Werkt scannen niet, gebruik dan ook Inverteren (de code staat 'negatief'). Scan de code: het antwoord staat erin.",
        "zichtbaar": "Zo ziet de QR-code er na bewerking uit:",
        "eigen": "Let op: de afbeelding is door het event aangeleverd. Het antwoord is wat de QR-code op die afbeelding oplevert.",
        "hints": ["Je ogen zien de QR-code nauwelijks. Een beeld kan aangepast worden.",
                  "Speel met belichting en de kleurkanalen in de bewerker.",
                  "Een QR-code is meestal zwart op wit. Probeer ook Inverteren, en scan dan met een telefoon."],
        "fysiek": "Optioneel: print deze QR-code in donkerblauw op zwart filament op een robot of sticker.",
    },
    "en": {
        "titel": "Robot QR",
        "intro": "Images can contain more than meets the eye. This robot carries a secret on its chest, but your eyes can barely see it.",
        "opdracht": "Open beeldbewerker/index.html on the computer: the image is already loaded. Edit it until you recognise something. "
                    "Scan the result with your phone and write down the answer.",
        "oplossing": "The QR code is dark blue on black. Raise brightness and contrast, or set the blue channel high and the others "
                     "low, until the pattern is sharp. If scanning fails, also use Invert (the code is 'negative'). Scan the code: the answer is inside.",
        "zichtbaar": "This is what the QR code looks like after editing:",
        "eigen": "Note: the image was supplied by the event. The answer is whatever the QR code in that image gives.",
        "hints": ["Your eyes can barely see the QR code. An image can be adjusted.",
                  "Play with exposure and the colour channels in the editor.",
                  "A QR code is usually black on white. Also try Invert, then scan with a phone."],
        "fysiek": "Optional: print this QR code in dark blue on black filament on a robot or sticker.",
    },
}


def maak_qr(antwoord: str):
    return segno.make(antwoord, error="h")


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, schaal = params["antwoord"], params["schaal"]
    if not antwoord.strip():
        raise ValueError("Het antwoord mag niet leeg zijn")
    eigen = params.get("afbeelding", "")  # afbeelding van het event, bv. een foto van de robot
    if eigen and not Path(eigen).is_file():
        raise ValueError(f"afbeelding '{eigen}' bestaat niet")
    qr = maak_qr(antwoord)
    qr.save(str(uit / "qr.png"), scale=schaal, border=2, dark=params["kleur"], light="#000000")
    gebruik(uit, params["taal"], "beeldbewerker", opties={"beeldbewerker": {"afbeelding": eigen or str(uit / "qr.png")}})

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    p.regel(t["opdracht"])
    if not eigen:  # de gegenereerde code staat ook op papier; een eigen foto zit enkel in de beeldbewerker
        breedte = 12 * cm
        p.ruimte(breedte)
        p.c.drawImage(str(uit / "qr.png"), MARGE, p.y, breedte, breedte)
        p.ruimte(10)
    p.opslaan()

    with tempfile.TemporaryDirectory() as tmp:
        zichtbaar = Path(tmp) / "zichtbaar.png"
        qr.save(str(zichtbaar), scale=schaal, border=2)
        b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"], t["fysiek"], t["zichtbaar"]] + ([t["eigen"]] if eigen else []),
                       t["hints"], params["taal"])
        b.ruimte(8 * cm)
        b.c.drawImage(str(zichtbaar), MARGE, b.y, 8 * cm, 8 * cm)
        b.opslaan()
    return antwoord


def check(params: dict) -> None:
    """Controleer dat de QR-code echt leesbaar is, als er een QR-lezer (zbarimg) beschikbaar is."""
    antwoord = params["antwoord"]
    assert maak_qr(antwoord).designator
    lezer = shutil.which("zbarimg")
    if not lezer:
        return
    with tempfile.TemporaryDirectory() as tmp:
        pad = Path(tmp) / "qr.png"
        maak_qr(antwoord).save(str(pad), scale=10, border=4)
        uitvoer = subprocess.run([lezer, "-q", "--raw", str(pad)], capture_output=True, text=True).stdout.strip()
    assert uitvoer == antwoord, f"QR gaf '{uitvoer}' in plaats van '{antwoord}'"
