"""Vigenère: een bericht met een onbekende sleutel. Het bekende begin verraadt de sleutel (aanval met bekende klare tekst)."""
import textwrap
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, Pdf, begeleider

ABC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

TEKST = {
    "titel": "Vigenère",
    "intro": "Een onderschept bericht van een geheim agent. Het is versleuteld met het Vigenèrecijfer: elke letter is "
             "verschoven zoals bij Caesar, maar de verschuiving verandert per letter volgens een sleutelwoord dat zich herhaalt. "
             "Alleen letters tellen mee voor de sleutel, spaties niet.",
    "bericht": "Het bericht",
    "bekend": "Wat we weten: elk bericht van deze agenten begint met",
    "vraag": "Vind de sleutel, ontcijfer het bericht en typ het antwoord in de kluis.",
    "tabel": "Vigenèretabel: rij = sleutelletter, kolom = klare letter, in het vak de versleutelde letter",
    "body_bekend": "Elk bericht begint met:",
    "oplossing": [
        "Vergelijk het bericht met het bekende begin '{bekend}'. Per letter: verschuiving = versleuteld - klaar (A = 0). "
        "Dat geeft {reeks}: de sleutel is {sleutel}.",
        "Ontcijferd: {klaar}",
    ],
    "afleiding": "Afleiding van de sleutel",
    "hints": [
        "Zet de eerste letters van het bericht onder het begin dat je kent. Hoeveel plaatsen is elke letter verschoven?",
        "Schrijf elke verschuiving als letter (0 = A, 1 = B, ...). Zie je een woord dat zich herhaalt? Dat is de sleutel.",
        "Ontcijferen: schuif elke letter terug met de sleutelletter eronder. Spaties tellen niet mee voor de sleutel.",
    ],
}


def klare_tekst(params: dict) -> str:
    return (f"{params['bekend']} jouw volgende opdracht staat klaar het antwoord voor de kluis is {params['antwoord']} "
            "vernietig dit bericht").upper()


def vigenere(tekst: str, sleutel: str, richting: int = 1) -> str:
    """Versleutel (richting 1) of ontcijfer (-1). Enkel letters A-Z schuiven en laten de sleutel opschuiven."""
    uit, i = [], 0
    for ch in tekst:
        if ch in ABC:
            uit.append(ABC[(ABC.index(ch) + richting * ABC.index(sleutel[i % len(sleutel)])) % 26])
            i += 1
        else:
            uit.append(ch)
    return "".join(uit)


def controleer(params: dict) -> tuple[str, str]:
    sleutel = params["sleutel"].upper()
    if not (sleutel.isalpha() and sleutel.isascii() and 3 <= len(sleutel) <= 8):
        raise ValueError("sleutel moet 3 tot 8 letters A-Z zijn")
    if not all(ch in ABC or ch == " " for ch in params["antwoord"].upper()):
        raise ValueError("antwoord mag enkel letters en spaties bevatten")
    bekend = params["bekend"].upper()
    if not all(ch in ABC or ch == " " for ch in bekend) or sum(ch in ABC for ch in bekend) < 2 * len(sleutel):
        raise ValueError("bekend moet uit letters en spaties bestaan, met minstens twee keer zo veel letters als de sleutel")
    return sleutel, bekend


def verschuivingen(versleuteld: str, bekend: str) -> list[tuple[str, str, int]]:
    """Per letter van het bekende begin: (versleuteld, klaar, verschuiving)."""
    paren = [(c, k) for c, k in zip(versleuteld, bekend) if k in ABC]
    return [(c, k, (ABC.index(c) - ABC.index(k)) % 26) for c, k in paren]


def tabula_recta(p: Pdf) -> None:
    """26 x 26 Vigenèretabel met een kopregel en kopkolom."""
    cel = min(0.62 * cm, (595 - 2 * MARGE) / 27)
    x0, y0 = MARGE, p.y
    for r in range(27):
        for k in range(27):
            x, y = x0 + k * cel, y0 - (r + 1) * cel
            if r == 0 or k == 0:
                p.c.setFillGray(0.85)
                p.c.rect(x, y, cel, cel, fill=1, stroke=0)
                p.c.setFillGray(0)
            if r == 0 and k == 0:
                continue
            letter = ABC[k - 1] if r == 0 else ABC[r - 1] if k == 0 else ABC[(r - 1 + k - 1) % 26]
            p.c.setFont("Helvetica-Bold" if r == 0 or k == 0 else "Helvetica", 7.5)
            p.c.drawCentredString(x + cel / 2, y + cel * 0.3, letter)
    p.c.setLineWidth(0.3)
    p.c.grid([x0 + k * cel for k in range(28)], [y0 - r * cel for r in range(28)])
    p.ruimte(27 * cel + 8)


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    sleutel, bekend = controleer(params)
    klaar = klare_tekst(params)
    versleuteld = vigenere(klaar, sleutel)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"], 11)
    p.kop(t["bericht"])
    p.mono("\n".join(textwrap.wrap(versleuteld, 60)), 12)  # afbreken op spaties: woordgrenzen zijn een aanwijzing
    p.regel(f"{t['bekend']} {bekend}", 11)
    p.regel(t["vraag"], 11)
    p.ruimte(4)
    p.regel(t["tabel"], 9)
    tabula_recta(p)
    p.opslaan()

    stappen = verschuivingen(versleuteld, bekend)
    reeks = "".join(ABC[s] for _, _, s in stappen)
    oplossing = [t["oplossing"][0].format(bekend=bekend.lower(), reeks=reeks, sleutel=sleutel),
                 t["oplossing"][1].format(klaar=klaar.lower())]
    b = begeleider(uit / "begeleider.pdf", t["titel"], params["antwoord"], oplossing, t["hints"])
    b.kop(t["afleiding"])
    b.tabel(("versleuteld", "klaar", "verschuiving", "sleutelletter"),
            [(c, k, str(s), ABC[s]) for c, k, s in stappen], (1, 1, 1, 1), 9)
    b.opslaan()

    if params.get("digitaal"):
        body = """  <div class="kaart">
    <h2>Het bericht</h2>
    <p id="bericht" class="antwoordbalk" style="font-size:20px;letter-spacing:.08em"></p>
    <p class="klein" id="bekend"></p>
  </div>
  <div class="kaart">
    <h2>Probeer een sleutel</h2>
    <div class="rij" style="margin-top:0"><input type="text" id="sleutel" maxlength="12" spellcheck="false" autocapitalize="characters" placeholder="SLEUTEL" aria-label="Sleutel"></div>
    <p class="klein">Ontcijferd met deze sleutel:</p>
    <p id="klaar" class="antwoordbalk" style="font-size:20px;letter-spacing:.08em">-</p>
  </div>
  <div class="kaart">
    <h2>Het alfabet</h2>
    <div id="alfabet" style="display:grid;grid-template-columns:repeat(13,1fr);gap:4px;font-family:var(--mono);text-align:center"></div>
  </div>"""
        css = "#bericht,#klaar{word-break:normal}"  # woorden niet middenin afbreken: woordgrenzen zijn een aanwijzing
        schrijf(uit, t["titel"], "Vind de sleutel met het begin dat je kent, en ontcijfer de rest.", body,
                Path(__file__).parent / "digitaal.js", {"bericht": versleuteld, "bekend": bekend}, t["hints"], css)
    return params["antwoord"]


def check(params: dict) -> None:
    sleutel, bekend = controleer(params)
    klaar = klare_tekst(params)
    versleuteld = vigenere(klaar, sleutel)
    assert vigenere(versleuteld, sleutel, -1) == klaar
    # het bekende begin is lang genoeg om de sleutel te zien herhalen, en geeft precies de sleutel
    reeks = "".join(ABC[s] for _, _, s in verschuivingen(versleuteld, bekend))
    assert reeks.startswith(sleutel * 2)
    assert params["antwoord"].upper() in klaar
