"""Meerdere lagen codering (binair, hex, base64, ...) om een antwoord heen."""
from pathlib import Path

from jr.pdf import Pdf, begeleider
from jr import codecs as c
from jr.shared import gebruik

# naam -> (inpakken, uitpakken, uitleg voor deelnemers)
LAGEN = {
    "binair": (c.naar_binair, c.van_binair, "binair (nullen en enen)"),
    "hex": (c.naar_hex, c.van_hex, "hexadecimaal"),
    "base64": (c.naar_base64, c.van_base64, "Base64"),
    "rot13": (lambda s: c.rot(s, 13), lambda s: c.rot(s, 13), "ROT13"),
    "morse": (c.naar_morse, c.van_morse, "morse"),
}

TEKST = {
    "nl": {
        "titel": "Laag na laag",
        "verhaal": "Dit bericht lijkt moeilijk te ontcijferen, alsof iemand het meerdere lagen diep heeft verborgen.",
        "bericht": "Het bericht:",
        "tip": "Gebruik de decoder op de computer. Het bericht staat ook in bericht.txt om te kopieren.",
        "oplossing": "{n} lagen. Pak ze uit in deze volgorde: {volgorde}.",
        "hints": ["Kijk naar hoe het bericht eruitziet. Welke soort code is dit?",
                  "Als je een laag hebt uitgepakt, ziet het resultaat er weer als code uit. Ga door.",
                  "Zet in de decoder meerdere stappen na elkaar."],
    },
    "en": {
        "titel": "Layer after layer",
        "verhaal": "This message seems hard to decode, as if someone hid it several layers deep.",
        "bericht": "The message:",
        "tip": "Use the decoder on the computer. The message is also in bericht.txt for copying.",
        "oplossing": "{n} layers. Unpack them in this order: {volgorde}.",
        "hints": ["Look at what the message looks like. What kind of code is it?",
                  "When you unpacked a layer, the result may look like code again. Keep going.",
                  "Chain several steps in the decoder."],
    },
}


def controleer_lagen(lagen: list[str]) -> None:
    onbekend = [x for x in lagen if x not in LAGEN]
    if onbekend or not lagen:
        raise ValueError(f"Onbekende lagen {onbekend}. Mogelijk: {', '.join(LAGEN)}")


def pak_in(antwoord: str, lagen: list[str]) -> str:
    s = antwoord
    for laag in lagen:
        s = LAGEN[laag][0](s)
    return s


def pak_uit(bericht: str, lagen: list[str]) -> str:
    s = bericht
    for laag in reversed(lagen):
        s = LAGEN[laag][1](s)
    return s


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, lagen = params["antwoord"], params["lagen"]
    controleer_lagen(lagen)
    if "morse" in lagen and not all(ch.upper() in c.MORSE for ch in antwoord) and lagen[0] == "morse":
        raise ValueError("Morse ondersteunt enkel letters, cijfers en '-' in het antwoord")
    bericht = pak_in(antwoord, lagen)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["verhaal"])
    p.kop(t["bericht"])
    p.mono(bericht)
    p.regel(t["tip"])
    p.opslaan()
    (uit / "bericht.txt").write_text(bericht + "\n")

    volgorde = " -> ".join(LAGEN[x][2] for x in reversed(lagen))
    stappen = []
    s = bericht
    for laag in reversed(lagen):
        s = LAGEN[laag][1](s)
        stappen.append(f"Na {LAGEN[laag][2]}: {s if len(s) < 120 else s[:117] + '...'}")
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord,
                   [t["oplossing"].format(n=len(lagen), volgorde=volgorde)] + stappen, t["hints"], params["taal"])
    b.opslaan()
    gebruik(uit, params["taal"], "decoder", "spiekbrief")
    return antwoord


def check(params: dict) -> None:
    lagen = params["lagen"]
    controleer_lagen(lagen)
    assert pak_uit(pak_in(params["antwoord"], lagen), lagen) == params["antwoord"]
