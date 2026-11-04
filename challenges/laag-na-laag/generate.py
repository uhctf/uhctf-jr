"""Meerdere lagen codering (binair, hex, base64, ...) om een antwoord heen."""
from pathlib import Path

from jr.digitaal import schrijf
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
        "verhaal": "Dit bericht zit in lagen verstopt.",
        "bericht": "Het bericht:",
        "tip": "Pak de lagen een voor een uit met de decoder.",
        "oplossing": "{n} lagen. Pak ze uit in deze volgorde: {volgorde}.",
        "hints": ["Kijk naar hoe het bericht eruitziet. Welke soort code is dit?",
                  "Als je een laag hebt uitgepakt, ziet het resultaat er weer als code uit. Ga door.",
                  "Zet in de decoder meerdere stappen na elkaar."],
        "hint_rot": "Lees je al woorden, maar zijn het onzin? Dan zijn de letters verschoven: probeer ROT-N in de decoder (met 13).",
    },
    "en": {
        "titel": "Layer after layer",
        "verhaal": "This message is hidden in layers.",
        "bericht": "The message:",
        "tip": "Unpack the layers one by one with the decoder.",
        "oplossing": "{n} layers. Unpack them in this order: {volgorde}.",
        "hints": ["Look at what the message looks like. What kind of code is it?",
                  "When you unpacked a layer, the result may look like code again. Keep going.",
                  "Chain several steps in the decoder."],
        "hint_rot": "Do you see word-like text that makes no sense? Then the letters were shifted: try ROT-N in the decoder (with 13).",
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
    hints = t["hints"] + ([t["hint_rot"]] if "rot13" in lagen else [])  # ROT13 herken je niet aan het uiterlijk: extra hint

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
                   [t["oplossing"].format(n=len(lagen), volgorde=volgorde)] + stappen, hints, params["taal"])
    b.opslaan()
    gebruik(uit, params["taal"], "decoder", "spiekbrief")
    if params.get("digitaal"):
        digitaal(bericht, uit, t, hints)
    return antwoord


def digitaal(bericht: str, uit: Path, t: dict, hints: list[str]) -> None:
    """Pagina met het bericht om te kopiëren en een knop die het in de decoder opent. De decoder staat in decoder/ naast de pagina."""
    body = """  <div class="kaart">
    <h2>Het bericht</h2>
    <textarea id="bericht" rows="7" readonly spellcheck="false"></textarea>
    <div class="rij">
      <button id="kopieer" type="button">Kopieer</button>
      <a id="decoder" href="decoder/index.html"><button class="primair" type="button">Open in de decoder</button></a>
      <span class="klein" id="gekopieerd"></span>
    </div>
  </div>"""
    schrijf(uit, t["titel"], t["verhaal"], body, Path(__file__).parent / "digitaal.js", {"bericht": bericht}, hints)


def check(params: dict) -> None:
    lagen = params["lagen"]
    controleer_lagen(lagen)
    assert pak_uit(pak_in(params["antwoord"], lagen), lagen) == params["antwoord"]
