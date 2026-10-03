"""Spiekbrief over coderingen. De voorbeelden worden met dezelfde code berekend als de uitdagingen gebruiken."""
from pathlib import Path

from reportlab.lib.units import cm

from jr import codecs as c
from jr.pdf import MARGE, W, Pdf

TEKST = {
    "nl": {
        "titel": "Spiekbrief codes",
        "invoer": "Invoer", "actie": "Actie", "uitvoer": "Uitvoer", "sleutel": "Sleutel",
        "naar": "naar", "van": "van",
        "binair": ("Binair", "Een tekst bestaat uit tekens. Elk standaardteken wordt voorgesteld door acht cijfers, 0 of 1: één byte."),
        "hex": ("Hexadecimaal", "Een getalsysteem met 16 cijfers (0-9 en A-F). Twee hex-tekens zijn samen één byte, een compacte manier om bytes op te schrijven."),
        "base64": ("Base64", "Zet gegevens om in tekst met 64 veilige tekens (A-Z, a-z, 0-9, + en /). Het eindigt vaak op = of ==."),
        "rot": ("ROT-N (Caesar)", "Elke letter wordt N plaatsen in het alfabet verschoven. ROT13 (N = 13) is de bekendste. Terugdraaien kan met 26 - N."),
        "xor": ("XOR met een sleutel", "Combineert de gegevens byte per byte met een sleutel. De bewerking is omkeerbaar: met dezelfde sleutel krijg je de oorspronkelijke tekst terug. Het resultaat schrijven we in hex."),
        "morse": ("Morse", "Elk teken is een unieke combinatie van punten en strepen. Een spatie scheidt tekens, een / scheidt woorden."),
        "naar_binair": "naar binair", "van_binair": "van binair", "naar_hex": "naar hex", "van_hex": "van hex",
        "naar_base64": "naar Base64", "van_base64": "van Base64", "van_xor": "XOR (hex naar tekst)", "naar_xor": "XOR (tekst naar hex)",
    },
    "en": {
        "titel": "Codes cheat sheet",
        "invoer": "Input", "actie": "Action", "uitvoer": "Output", "sleutel": "Key",
        "naar": "to", "van": "from",
        "binair": ("Binary", "A text is made of characters. Every standard character is represented by eight digits, 0 or 1: one byte."),
        "hex": ("Hexadecimal", "A number system with 16 digits (0-9 and A-F). Two hex characters make one byte, a compact way to write bytes."),
        "base64": ("Base64", "Turns data into text using 64 safe characters (A-Z, a-z, 0-9, + and /). It often ends with = or ==."),
        "rot": ("ROT-N (Caesar)", "Every letter is shifted N places in the alphabet. ROT13 (N = 13) is the best known. To undo it, use 26 - N."),
        "xor": ("XOR with a key", "Combines the data byte by byte with a key. The operation is reversible: with the same key you get the original text back. We write the result in hex."),
        "morse": ("Morse", "Every character is a unique combination of dots and dashes. A space separates characters, a / separates words."),
        "naar_binair": "to binary", "van_binair": "from binary", "naar_hex": "to hex", "van_hex": "from hex",
        "naar_base64": "to Base64", "van_base64": "from Base64", "van_xor": "XOR (hex to text)", "naar_xor": "XOR (text to hex)",
    },
}


def tabel(p: Pdf, kop: tuple[str, ...], rijen: list[tuple[str, ...]], breedtes: tuple[float, ...]) -> None:
    """Teken een eenvoudige tabel op de huidige positie."""
    hoogte = 0.7 * cm
    totaal = sum(breedtes)
    for i, rij in enumerate([kop] + rijen):
        y = p.y - hoogte
        x = MARGE
        for tekst, br in zip(rij, breedtes):
            br = br / totaal * (W - 2 * MARGE)
            p.c.setFont("Helvetica-Bold" if i == 0 else "Courier", 10)
            p.c.rect(x, y, br, hoogte)
            p.c.drawString(x + 4, y + 0.22 * cm, tekst)
            x += br
        p.y = y
    p.ruimte(16)


def sectie(p: Pdf, t: dict, sleutel: str) -> None:
    naam, uitleg = t[sleutel]
    if p.y < 7 * cm:
        p.pagina(t["titel"])
    p.kop(naam)
    p.regel(uitleg, 11)


def generate(params: dict, uit: Path) -> None:
    t = TEKST.get(params["taal"], TEKST["nl"])
    uit.mkdir(parents=True, exist_ok=True)
    p = Pdf(uit / "spiekbrief.pdf", t["titel"])
    kop = (t["invoer"], t["actie"], t["uitvoer"])
    b = (3, 3, 4)

    sectie(p, t, "binair")
    tabel(p, kop, [("A", t["naar_binair"], c.naar_binair("A")), (c.naar_binair("B"), t["van_binair"], "B")], b)

    sectie(p, t, "hex")
    tabel(p, kop, [("hello", t["naar_hex"], c.naar_hex("hello").upper()),
                   (c.naar_hex("world").upper(), t["van_hex"], "world")], b)

    sectie(p, t, "base64")
    tabel(p, kop, [("Flag", t["naar_base64"], c.naar_base64("Flag")), (c.naar_base64("Hello!"), t["van_base64"], "Hello!")], b)

    sectie(p, t, "rot")
    tabel(p, (t["invoer"], "N", t["uitvoer"]),
          [("ABCDE", "1", c.rot("ABCDE", 1)), ("SCIENCE", "13", c.rot("SCIENCE", 13)),
           (c.rot("WETENSCHAP", 13), "13", "WETENSCHAP")], (3, 2, 4))

    sectie(p, t, "xor")
    tabel(p, (t["invoer"], t["sleutel"], t["uitvoer"]),
          [("hello", "key", c.xor_naar_hex("hello", "key").upper()),
           (c.xor_naar_hex("hello", "key").upper(), "key", "hello")], (4, 2, 4))

    sectie(p, t, "morse")
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    half = (len(letters) + 1) // 2
    for i in range(half):
        rij = [letters[i], c.MORSE[letters[i]]]
        rij += [letters[i + half], c.MORSE[letters[i + half]]] if i + half < len(letters) else ["", ""]
        # compacte tabel: 4 kolommen, één rij per keer
        hoogte = 0.5 * cm
        y, x = p.y - hoogte, MARGE
        for j, tekst in enumerate(rij):
            br = (W - 2 * MARGE) * (0.1 if j % 2 == 0 else 0.4)
            p.c.setFont("Courier", 10)
            p.c.rect(x, y, br, hoogte)
            p.c.drawString(x + 4, y + 0.14 * cm, tekst)
            x += br
        p.y = y
    p.opslaan()


def check(params: dict) -> None:
    """De voorbeelden moeten omkeerbaar zijn."""
    assert c.van_binair(c.naar_binair("B")) == "B"
    assert c.van_hex(c.naar_hex("world")) == "world"
    assert c.van_base64(c.naar_base64("Hello!")) == "Hello!"
    assert c.rot(c.rot("WETENSCHAP", 13), 13) == "WETENSCHAP"
    assert c.xor_van_hex(c.xor_naar_hex("hello", "key"), "key") == "hello"
    assert c.van_morse(c.naar_morse("cyber")) == "cyber"
