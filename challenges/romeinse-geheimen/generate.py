"""Caesarcijfer: elk woord van het antwoord is met een vast aantal letters verschoven, elk woord met een eigen verschuiving."""
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, Pdf, begeleider
from jr import codecs
from jr.shared import gebruik

TEKST = {
    "nl": {
        "titel": "Romeinse geheimen",
        "verhaal": "Een archeoloog vond een bericht dat lijkt te zijn gecodeerd door een keizer.",
        "bericht": "Het bericht:",
        "tip": "Elke letter is evenveel plaatsen verschoven. Zet in de onderste rij van de strook het alfabet, maar begin op een andere plaats.",
        "tip_decoder": "Elke letter is evenveel plaatsen verschoven. Zet in de onderste rij van de strook het alfabet, maar begin op een andere plaats. Of gebruik de decoder op de laptop.",
        "oefen_kop": "Eerst oefenen",
        "oefen_hint": "Hint: {hint}",
        "oefen_tip": "Deze woorden zijn net zo verschoven als het bericht. Raad er één en tel hoeveel plaatsen elke letter is opgeschoven.",
        "tip_meer": "Elk woord is met een ander aantal plaatsen verschoven. Zet in de onderste rij van de strook het alfabet, maar begin op een andere plaats. Zoek de verschuiving van elk woord apart.",
        "tip_decoder_meer": "Elk woord is met een ander aantal plaatsen verschoven. Zet in de onderste rij van de strook het alfabet, maar begin op een andere plaats. Zoek de verschuiving van elk woord apart. Of gebruik de decoder op de laptop.",
        "oefen_tip_meer": "Elk woord van het bericht heeft een eigen oefenwoord met dezelfde verschuiving. Oefenwoord 1 hoort bij woord 1, enzovoort. Raad het oefenwoord en tel hoeveel plaatsen elke letter is opgeschoven.",
        "oplossing": "Verschuif elke letter {n} plaatsen vooruit in het alfabet (Caesar, ROT-{n} bij het ontcijferen).",
        "oplossing_woord": "Woord {i}: {code} is {n} plaatsen verschoven (ROT-{n} bij het ontcijferen): {woord}",
        "hints": ["Welke keizer gebruikte een geheimschrift waarbij je letters verschuift?",
                  "Het is een Caesarcijfer: in elk woord is elke letter een vast aantal plaatsen verschoven.",
                  "Bestaat het bericht uit meer woorden? Dan kan elk woord een andere verschuiving hebben. Zoek ze één voor één.",
                  "Probeer het met kleine getallen: verschuif 1, 2, 3 plaatsen."],
    },
    "en": {
        "titel": "Roman secrets",
        "verhaal": "An archaeologist found a message that seems to have been encoded by an emperor.",
        "bericht": "The message:",
        "tip": "Every letter moved the same number of places. In the bottom row of the strip, write the alphabet but start at a different place.",
        "tip_decoder": "Every letter moved the same number of places. In the bottom row of the strip, write the alphabet but start at a different place. Or use the decoder on the laptop.",
        "oefen_kop": "Practice first",
        "oefen_hint": "Hint: {hint}",
        "oefen_tip": "These words moved the same way as the message. Guess one and count how many places each letter moved.",
        "tip_meer": "Every word moved a different number of places. In the bottom row of the strip, write the alphabet but start at a different place. Find the shift of each word separately.",
        "tip_decoder_meer": "Every word moved a different number of places. In the bottom row of the strip, write the alphabet but start at a different place. Find the shift of each word separately. Or use the decoder on the laptop.",
        "oefen_tip_meer": "Every word of the message has its own practice word with the same shift. Practice word 1 goes with word 1, and so on. Guess the practice word and count how many places each letter moved.",
        "oplossing": "Shift every letter {n} places forward in the alphabet (Caesar, ROT-{n} when decoding).",
        "oplossing_woord": "Word {i}: {code} moved {n} places (ROT-{n} when decoding): {woord}",
        "hints": ["Which emperor used a secret writing where you shift the letters?",
                  "It is a Caesar cipher: in every word each letter is shifted a fixed number of places.",
                  "Does the message have more words? Then each word can have a different shift. Find them one by one.",
                  "Try small numbers: shift 1, 2, 3 places."],
    },
}


def versleutel(antwoord: str, n: int) -> str:
    # Deelnemers ontcijferen met +n, dus het bericht is -n verschoven.
    return codecs.rot(antwoord.upper(), -n)


def woorden_van(antwoord: str) -> list[str]:
    return antwoord.replace("-", " ").split()


def verschuivingen(params: dict) -> tuple[list[int], bool]:
    """De verschuiving per woord, en of elk woord zijn eigen verschuiving heeft.
    Eén getal in de lijst geldt voor alle woorden; anders moet er één getal per woord zijn en moeten ze verschillen."""
    woorden = woorden_van(params["antwoord"])
    if not woorden:
        raise ValueError("Het antwoord mag niet leeg zijn")
    ns = [int(n) for n in params["verschuivingen"]]
    if not ns:
        raise ValueError("verschuivingen mag niet leeg zijn")
    if any(n % 26 == 0 for n in ns):
        raise ValueError("een verschuiving mag geen veelvoud van 26 zijn (dan is het woord niet versleuteld)")
    if len(ns) == 1:
        return ns * len(woorden), False
    if len(ns) != len(woorden):
        raise ValueError(f"het antwoord heeft {len(woorden)} woorden, maar er zijn {len(ns)} verschuivingen: "
                         "geef één verschuiving per woord (of één voor alle woorden)")
    if len({n % 26 for n in ns}) != len(ns):
        raise ValueError("de verschuivingen moeten verschillen")
    return ns, True


def oefen(params: dict, ns: list[int], apart: bool) -> list[tuple[int, str]]:
    """De versleutelde oefenwoorden met hun nummer. Bij aparte verschuivingen hoort oefenwoord i bij woord i; anders gelden ze allemaal voor de ene verschuiving."""
    ws = list(params["oefenwoorden"])
    if apart and len(ws) > len(ns):
        raise ValueError(f"er zijn {len(ws)} oefenwoorden voor {len(ns)} woorden: geef er hoogstens één per woord")
    return [(i, versleutel(w, ns[i - 1] if apart else ns[0])) for i, w in enumerate(ws, 1) if w]


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord = params["antwoord"]
    woorden = woorden_van(antwoord)
    ns, apart = verschuivingen(params)
    codes = [versleutel(w, n) for w, n in zip(woorden, ns)]
    bericht = " ".join(codes)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["verhaal"])
    p.kop(t["bericht"])
    p.c.setFont("Courier-Bold", 28)
    x = MARGE
    for code in codes:  # de woorden naast elkaar, op een nieuwe regel als het niet meer past
        breedte = p.c.stringWidth(code + " ", "Courier-Bold", 28)
        if x > MARGE and x + breedte > 595 - MARGE:
            x = MARGE
            p.ruimte(36)
        p.c.drawString(x, p.y - 10, code)
        x += breedte
    p.ruimte(50)
    oefenwoorden = oefen(params, ns, apart)
    if oefenwoorden:
        p.kop(t["oefen_kop"])
        p.regel(t["oefen_tip_meer"] if apart else t["oefen_tip"])
        if params["oefenhint"]:
            p.c.setFont("Helvetica-Bold", 12)
            p.regel(t["oefen_hint"].format(hint=params["oefenhint"]))
        p.c.setFont("Courier-Bold", 20)
        p.c.drawString(MARGE, p.y - 6, "     ".join(f"{i}: {w}" if apart else w for i, w in oefenwoorden))
        p.ruimte(34)
    tip = ("tip_decoder" if params["met_decoder"] else "tip") + ("_meer" if apart else "")
    p.regel(t[tip])
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

    if apart:
        uitleg = [t["oplossing_woord"].format(i=i, code=c, n=n, woord=w.upper())
                  for i, (c, n, w) in enumerate(zip(codes, ns, woorden), 1)]
    else:
        uitleg = [t["oplossing"].format(n=ns[0])]
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [f"Bericht: {bericht}"] + uitleg, t["hints"], params["taal"])
    b.opslaan()
    if params["met_decoder"]:
        gebruik(uit, params["taal"], "decoder", "spiekbrief")
    if params.get("digitaal"):
        digitaal(params, uit, t)
    return antwoord


def digitaal(params: dict, uit: Path, t: dict) -> None:
    """Caesarwiel op het scherm als hulpmiddel: draai de ring, tik zelf een woord in en het wiel vertaalt het met de gekozen verschuiving. De pagina bevat geen bericht, oefenwoorden of verschuiving: enkel een invoerveld."""
    css = """
.wiel-rij{display:grid;grid-template-columns:minmax(260px,380px) 1fr;gap:28px;align-items:start}
@media(max-width:760px){.wiel-rij{grid-template-columns:1fr}}
#wiel{width:100%;height:auto;display:block}
#wiel .ring{stroke:var(--lijn);stroke-width:3}
#wiel .r152{fill:var(--cyaan-zacht)}#wiel .r120{fill:var(--zacht)}#wiel .r80{fill:#fff}
#wiel .buiten{font:900 16px ui-monospace,Menlo,Consolas,monospace;fill:#222}
#wiel .binnen{font:900 16px ui-monospace,Menlo,Consolas,monospace;fill:var(--magenta-donker)}
.schuif-rij{display:flex;gap:12px;align-items:center;flex-wrap:wrap;margin-top:12px}
#schuif{flex:1;min-width:140px;accent-color:var(--magenta);height:28px}
.getal{font-family:var(--mono);font-size:22px;font-weight:900}
#invoer{width:100%;font-family:var(--mono);font-size:24px;font-weight:900;text-transform:uppercase;box-sizing:border-box}
#uitvoer{font-size:30px;min-height:1.4em;word-break:break-all}
"""
    body = """  <div class="kaart">
    <h2>Caesarwiel</h2>
    <div class="wiel-rij">
      <div>
        <svg id="wiel" viewBox="0 0 320 320" role="img" aria-label="Caesarwiel"></svg>
        <div class="schuif-rij">
          <button id="links" type="button" aria-label="Een plaats terug">&larr;</button>
          <input id="schuif" type="range" min="0" max="25" value="0" aria-label="Verschuiving">
          <button id="rechts" type="button" aria-label="Een plaats vooruit">&rarr;</button>
        </div>
        <p>Verschuiving: <span class="getal" id="getal">0</span></p>
      </div>
      <div>
        <h2>Vertaler</h2>
        <p class="klein" style="margin-top:0">Tik een woord in. Het wiel vertaalt het met de verschuiving die je gekozen hebt.</p>
        <input id="invoer" type="text" autocomplete="off" autocapitalize="characters" spellcheck="false" aria-label="Woord om te vertalen">
        <div id="uitvoer" class="antwoordbalk" aria-live="polite"></div>
      </div>
    </div>
  </div>"""
    gegevens = {}  # niets in de pagina: de kinderen tikken zelf in wat ze willen vertalen
    schrijf(uit, t["titel"], "Draai het wiel, tik een woord in en lees de vertaling.", body, Path(__file__).parent / "digitaal.js", gegevens, t["hints"], css)


def check(params: dict) -> None:
    woorden = woorden_van(params["antwoord"])
    ns, _ = verschuivingen(params)
    for w, n in zip(woorden, ns):
        assert codecs.rot(versleutel(w, n), n) == w.upper()
