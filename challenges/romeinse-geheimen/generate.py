"""Caesarcijfer: een woord, verschoven met een vast aantal letters."""
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
        "oplossing": "Verschuif elke letter {n} plaatsen vooruit in het alfabet (Caesar, ROT-{n} bij het ontcijferen).",
        "hints": ["Welke keizer gebruikte een geheimschrift waarbij je letters verschuift?",
                  "Het is een Caesarcijfer: elke letter is een vast aantal plaatsen verschoven.",
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
        "oplossing": "Shift every letter {n} places forward in the alphabet (Caesar, ROT-{n} when decoding).",
        "hints": ["Which emperor used a secret writing where you shift the letters?",
                  "It is a Caesar cipher: every letter is shifted a fixed number of places.",
                  "Try small numbers: shift 1, 2, 3 places."],
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
    oefen = [w for w in params["oefenwoorden"] if w]
    if oefen:
        p.kop(t["oefen_kop"])
        p.regel(t["oefen_tip"])
        if params["oefenhint"]:
            p.c.setFont("Helvetica-Bold", 12)
            p.regel(t["oefen_hint"].format(hint=params["oefenhint"]))
        p.c.setFont("Courier-Bold", 20)
        p.c.drawString(MARGE, p.y - 6, "     ".join(versleutel(w, n) for w in oefen))
        p.ruimte(34)
    p.regel(t["tip_decoder"] if params["met_decoder"] else t["tip"])
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
    if params["met_decoder"]:
        gebruik(uit, params["taal"], "decoder", "spiekbrief")
    if params.get("digitaal"):
        digitaal(params, bericht, n, uit, t)
    return antwoord


def digitaal(params: dict, bericht: str, n: int, uit: Path, t: dict) -> None:
    """Caesarwiel op het scherm: draai de ring tot de oefenwoorden gewone woorden zijn en lees dan het bericht. De verschuiving zelf staat niet in de pagina."""
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
#oefen{list-style:none;padding:0;display:grid;gap:6px;font-size:20px;margin:6px 0 20px}
#oefen li{display:flex;gap:10px;align-items:center}
#oefen .code{font-family:var(--mono);font-weight:900;background:#e4e4ec;padding:0 10px}
#oefen strong{font-family:var(--mono);background:var(--cyaan);border:3px solid var(--lijn);padding:0 10px}
#uitvoer{font-size:30px}
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
        <div id="oefen-kaart">
          <h2>Oefenen</h2>
          <p id="oefenhint" class="klein"></p>
          <ul id="oefen"></ul>
        </div>
        <h2>Het bericht</h2>
        <div id="uitvoer" class="antwoordbalk" aria-live="polite"></div>
      </div>
    </div>
  </div>"""
    gegevens = {"bericht": bericht, "oefen": [versleutel(w, n) for w in params["oefenwoorden"] if w], "hint": params["oefenhint"]}
    schrijf(uit, t["titel"], "Zoek de verschuiving en lees het bericht.", body, Path(__file__).parent / "digitaal.js", gegevens, t["hints"], css)


def check(params: dict) -> None:
    n = params["verschuiving"]
    assert codecs.rot(versleutel(params["antwoord"], n), n) == params["antwoord"].upper()
