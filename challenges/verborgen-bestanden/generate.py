"""Verborgen bestanden: een USB-stick met een vermomde afbeelding en een foto met extra bytes na het einde. Forensics met magic bytes."""
import base64
import io
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from jr.digitaal import schrijf
from jr.pdf import Pdf, begeleider

PNG_START = b"\x89PNG\r\n\x1a\n"
JPEG_EINDE = b"\xff\xd9"

# formaat, eerste bytes (hex), in tekst: zo herken je ze in de hexweergave
MAGIC = [
    ("PNG-afbeelding", "89 50 4E 47 0D 0A 1A 0A", ".PNG...."),
    ("JPEG-afbeelding", "FF D8 FF ... eindigt op FF D9", "ÿØÿ"),
    ("GIF-afbeelding", "47 49 46 38", "GIF8"),
    ("PDF-document", "25 50 44 46", "%PDF"),
    ("ZIP (ook .docx, .xlsx)", "50 4B 03 04", "PK.."),
    ("gewone tekst", "geen vaste start, leesbare letters", "Hallo ..."),
]

TEKST = {
    "titel": "Verborgen bestanden",
    "intro": "De politie vond een USB-stick van een verdachte. Er staan drie onschuldige bestanden op, maar de verdachte heeft er "
             "een geheim in verstopt, in twee delen. De naam van een bestand zegt niet wat erin zit: kijk naar de bytes.",
    "laptop": "Open Verborgen bestanden op de laptop. Bekijk elk bestand in de hexweergave, als tekst en als afbeelding.",
    "map": "De bestanden staan in de map usb/. Bekijk ze met een hexviewer, of met file, xxd of strings.",
    "bestanden": "Op de stick",
    "magic": "Magic bytes: zo begint een bestand van elk formaat",
    "antwoord": "Het antwoord is deel 1 en deel 2 met een koppelteken ertussen.",
    "oplossing": [
        "notities.txt begint met 89 50 4E 47: het is een PNG. Als afbeelding geopend staat er 'deel 1: {deel1}'.",
        "vakantie.jpg is een echte JPEG, maar na het einde (FF D9) volgt nog tekst: 'deel 2: {deel2}'.",
        "boodschappen.txt is gewone tekst, een afleider.",
        "Antwoord: {antwoord}.",
    ],
    "hints": [
        "De extensie (.txt, .jpg) is maar een naam. De eerste bytes van een bestand verraden het echte formaat: vergelijk ze met de tabel.",
        "notities.txt begint niet met tekst. Welk formaat begint met 89 50 4E 47? Open het bestand als dat formaat.",
        "Een JPEG eindigt altijd met FF D9. Kijk in de hexweergave of als tekst naar het einde van vakantie.jpg: staat er nog iets na?",
    ],
}

BOODSCHAPPEN = "Boodschappen\n- melk\n- brood\n- 6 eieren\n- kaas\n- appels\n- batterijen (AA)\n- chips voor zaterdag\n"


def delen(antwoord: str) -> tuple[str, str]:
    deel1, _, deel2 = antwoord.partition("-")
    if not (deel1.isalnum() and deel2.isalnum() and deel1.isascii() and deel2.isascii()):
        raise ValueError("antwoord moet twee delen van letters of cijfers zijn met één koppelteken ertussen, bv. 'magische-bytes'")
    return deel1, deel2


def vermomde_png(deel1: str) -> bytes:
    """Een PNG met het eerste deel in grote letters, alsof iemand een notitie heeft gefotografeerd."""
    img = Image.new("RGB", (640, 220), "#fffbe6")
    teken = ImageDraw.Draw(img)
    for y in range(60, 220, 40):  # lijntjes van een notitieblok
        teken.line([(20, y), (620, y)], fill="#b9d3f0", width=2)
    teken.text((40, 36), "deel 1:", fill="#333", font=ImageFont.load_default(size=40))
    teken.text((40, 110), deel1, fill="#b3007f", font=ImageFont.load_default(size=64))
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return buf.getvalue()


def foto_met_staart(deel2: str) -> bytes:
    """Een eenvoudige vakantiefoto (lucht, zon, zee) met na het JPEG-einde nog tekst."""
    img = Image.new("RGB", (360, 240))
    teken = ImageDraw.Draw(img)
    for y in range(150):
        teken.line([(0, y), (360, y)], fill=(255, 160 + y // 3, 90 + y))
    teken.ellipse([140, 80, 220, 160], fill="#ffd23f")
    for y in range(150, 240):
        teken.line([(0, y), (360, y)], fill=(20, 90 + (y - 150) // 2, 150))
    buf = io.BytesIO()
    img.save(buf, "JPEG", quality=70)
    return buf.getvalue() + f"\ndeel 2: {deel2}\n".encode()


def bestanden(antwoord: str) -> dict[str, bytes]:
    deel1, deel2 = delen(antwoord)
    return {"vakantie.jpg": foto_met_staart(deel2), "notities.txt": vermomde_png(deel1), "boodschappen.txt": BOODSCHAPPEN.encode()}


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    antwoord = params["antwoord"]
    deel1, deel2 = delen(antwoord)
    stick = bestanden(antwoord)
    (uit / "usb").mkdir(exist_ok=True)
    for naam, data in stick.items():
        (uit / "usb" / naam).write_bytes(data)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    p.regel(t["laptop"] if params.get("digitaal") else t["map"])
    p.kop(t["bestanden"])
    for naam, data in stick.items():
        p.regel(f"- {naam} ({len(data)} bytes)")
    p.kop(t["magic"])
    p.tabel(("Formaat", "Eerste bytes (hex)", "Als tekst"), [tuple(r) for r in MAGIC], (3, 4, 2), 11)
    p.regel(t["antwoord"])
    p.opslaan()

    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord,
                   [r.format(deel1=deel1, deel2=deel2, antwoord=antwoord) for r in t["oplossing"]], t["hints"])
    b.opslaan()

    if params.get("digitaal"):
        css = """
#lijst{display:flex;gap:12px;flex-wrap:wrap}
#lijst button.gekozen{background:var(--cyaan)}
#hex{background:#fff;border:3px solid var(--lijn);font-family:var(--mono);font-size:14px;line-height:1.5;padding:10px 14px;max-height:420px;overflow:auto;white-space:pre;margin:14px 0 0}
#hex .adres{color:var(--muted)}#hex .asc{color:var(--magenta-donker)}
#weergave img{max-width:100%;border:3px solid var(--lijn);margin-top:14px;display:block}
#weergave pre{white-space:pre-wrap;word-break:break-all;background:#fff;border:3px solid var(--lijn);padding:10px 14px;max-height:420px;overflow:auto;margin:14px 0 0}
#magic td,#magic th{border:2px solid var(--lijn);padding:4px 10px;text-align:left}#magic{border-collapse:collapse;font-size:15px}
#magic td:nth-child(2){font-family:var(--mono)}
"""
        body = """  <div class="kaart">
    <h2>Op de stick</h2>
    <div id="lijst"></div>
  </div>
  <div class="kaart">
    <h2 id="kop">Bestand</h2>
    <div class="rij" style="margin-top:0">
      <button type="button" id="toon-hex">Hex</button>
      <button type="button" id="toon-tekst">Als tekst</button>
      <button type="button" id="toon-beeld">Als afbeelding</button>
    </div>
    <div id="weergave"><p class="klein">Kies een bestand.</p></div>
  </div>
  <div class="kaart">
    <h2>Magic bytes</h2>
    <div style="overflow-x:auto"><table id="magic"></table></div>
  </div>"""
        data = {"bestanden": [{"naam": n, "b64": base64.b64encode(d).decode()} for n, d in stick.items()],
                "magic": [list(r) for r in MAGIC]}
        schrijf(uit, t["titel"], "Drie onschuldige bestanden? Kijk naar de bytes, niet naar de naam.", body,
                Path(__file__).parent / "digitaal.js", data, t["hints"], css)
    return antwoord


def check(params: dict) -> None:
    deel1, deel2 = delen(params["antwoord"])
    stick = bestanden(params["antwoord"])
    png = stick["notities.txt"]
    assert png.startswith(PNG_START) and Image.open(io.BytesIO(png)).format == "PNG"
    foto = stick["vakantie.jpg"]
    einde = foto.rindex(JPEG_EINDE)
    assert foto.startswith(b"\xff\xd8\xff") and Image.open(io.BytesIO(foto[:einde + 2])).format == "JPEG"
    assert f"deel 2: {deel2}".encode() in foto[einde + 2:]  # het tweede deel staat echt na het einde van de afbeelding
    lijst = stick["boodschappen.txt"].decode()  # de afleider is echte tekst, zonder een deel van het antwoord
    assert lijst.replace("\n", "").isprintable() and deel1 not in lijst and deel2 not in lijst
