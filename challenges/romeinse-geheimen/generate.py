"""Caesarcijfer: een woord, verschoven met een vast aantal letters."""
from pathlib import Path

from reportlab.lib.units import cm

from jr.pdf import MARGE, Pdf, begeleider
from jr import codecs
from jr.shared import gebruik

TEKST = {
    "nl": {
        "titel": "Romeinse geheimen",
        "verhaal": "Een archeoloog vond een bericht dat lijkt te zijn gecodeerd door een keizer.",
        "bericht": "Het bericht:",
        "tip": "Elke letter is een vast aantal plaatsen in het alfabet verschoven. Hoeveel? Gebruik de strook hieronder, "
               "of de decoder op de computer. Schrijf het antwoord op.",
        "oplossing": "Verschuif elke letter {n} plaatsen terug in het alfabet (Caesar, ROT-{n} bij het ontcijferen).",
        "hints": ["Welke keizer gebruikte een geheimschrift waarbij je letters verschuift?",
                  "Het is een Caesarcijfer: elke letter is een vast aantal plaatsen verschoven.",
                  "Probeer in de decoder de stap ROT-N met kleine getallen."],
    },
    "en": {
        "titel": "Roman secrets",
        "verhaal": "An archaeologist found a message that seems to have been encoded by an emperor.",
        "bericht": "The message:",
        "tip": "Every letter is shifted a fixed number of places in the alphabet. How many? Use the strip below, "
               "or the decoder on the computer. Write down the answer.",
        "oplossing": "Shift every letter {n} places back in the alphabet (Caesar, ROT-{n} when decoding).",
        "hints": ["Which emperor used a secret writing where you shift the letters?",
                  "It is a Caesar cipher: every letter is shifted a fixed number of places.",
                  "Try the ROT-N step in the decoder with small numbers."],
    },
}


def versleutel(antwoord: str, n: int) -> str:
    # Deelnemers ontcijferen met +n, dus het bericht is -n verschoven.
    return codecs.rot(antwoord.upper(), -n)


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, n = params["antwoord"], params["verschuiving"]
    if n % 26 == 0:
        raise ValueError("verschuiving mag geen veelvoud van 26 zijn (dan is het bericht niet versleuteld)")
    bericht = versleutel(antwoord, n)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["verhaal"])
    p.kop(t["bericht"])
    p.c.setFont("Courier-Bold", 28)
    p.c.drawString(MARGE, p.y - 10, bericht)
    p.ruimte(50)
    p.regel(t["tip"])
    p.ruimte(10)
    # Alfabetstrook: bovenste rij ingevuld, onderste rij leeg om de verschoven letters in te vullen.
    breedte = (595 - 2 * MARGE) / 26
    for i in range(26):
        x = MARGE + i * breedte
        p.c.rect(x, p.y - 0.9 * cm, breedte, 0.9 * cm)
        p.c.rect(x, p.y - 1.8 * cm, breedte, 0.9 * cm)
        p.c.setFont("Helvetica-Bold", 11)
        p.c.drawCentredString(x + breedte / 2, p.y - 0.62 * cm, chr(65 + i))
    p.opslaan()
    (uit / "bericht.txt").write_text(bericht + "\n")

    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord,
                   [f"Bericht: {bericht}", t["oplossing"].format(n=n)], t["hints"], params["taal"])
    b.opslaan()
    gebruik(uit, params["taal"], "decoder", "spiekbrief")
    return antwoord


def check(params: dict) -> None:
    n = params["verschuiving"]
    assert codecs.rot(versleutel(params["antwoord"], n), n) == params["antwoord"].upper()
