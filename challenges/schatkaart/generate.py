"""Schatkaart: te veel stippen op de kaart, raadsels wijzen de juiste aan. De letters bij die stippen spellen het antwoord."""
import random
import string
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, W, Pdf, begeleider

KOLOMMEN = "ABCDEFGHIJ"
RIJEN = 10

# Kolomraadsels: het antwoord is de eerste letter van het gezochte woord. Per kolom twee raadsels.
KOLOM = {
    "A": ["De eerste letter van het fruit waarvan één per dag de dokter weg houdt.",
          "De eerste letter van het dier dat van tak naar tak slingert en graag bananen eet."],
    "B": ["De eerste letter van het insect dat honing maakt.",
          "De eerste letter van het grote bruine dier dat in de winter slaapt en graag honing eet."],
    "C": ["De eerste letter van wat je krijgt op je verjaardag, ingepakt in mooi papier.",
          "De eerste letter van de grappenmaker in het circus met een rode neus."],
    "D": ["De eerste letter van het dier dat in sprookjes vuur spuwt.",
          "De eerste letter van het zoogdier in de zee dat graag springt en fluit."],
    "E": ["De eerste letter van het dier dat 'kwak' zegt.",
          "De eerste letter van het rode diertje dat noten verstopt en in bomen klimt."],
    "F": ["De eerste letter van het voertuig met twee wielen en trappers.",
          "De eerste letter van het blaasinstrument van de rattenvanger."],
    "G": ["De eerste letter van het dier met de langste nek.",
          "De eerste letter van het glimmende gele metaal in een schatkist."],
    "H": ["De eerste letter van het dier dat 'woef' zegt.",
          "De eerste letter van wat je tegen de zon op je hoofd draagt, met een brede rand."],
    "I": ["De eerste letter van wat je eet uit een hoorntje op een warme dag.",
          "De eerste letter van wat er uit een vulpen komt."],
    "J": ["De eerste letter van het kledingstuk dat je over je trui draagt als het koud is.",
          "De eerste letter van de eerste maand van het jaar."],
}
# Rijraadsels: het antwoord is een getal van 1 tot en met 10.
RIJ = {
    1: ["Het aantal zonnen aan de hemel overdag.", "Het aantal neuzen in je gezicht."],
    2: ["Het aantal wielen van een fiets.", "Het aantal ogen van een mens."],
    3: ["Het aantal hoeken van een driehoek.", "Het aantal biggetjes in het sprookje van de wolf en de drie huisjes."],
    4: ["Het aantal poten van een hond.", "Het aantal seizoenen in een jaar."],
    5: ["Het aantal vingers aan één hand.", "Het aantal ringen in het logo van de Olympische Spelen."],
    6: ["Het aantal poten van een insect.", "Het aantal zijden van een dobbelsteen."],
    7: ["Het aantal dagen in een week.", "Het aantal kleuren in de regenboog."],
    8: ["Het aantal poten van een spin.", "Het aantal armen van een octopus."],
    9: ["Drie keer drie.", "Het aantal letters in het woord 'beveiligd'."],
    10: ["Het aantal vingers aan twee handen.", "Het aantal letters in het woord 'wachtwoord'."],
}

TEKST = {
    "titel": "Schatkaart",
    "intro": "De kaart staat vol stippen, maar alleen de stippen van de raadsels zijn goed. Elk raadsel geeft een letter (de kolom, bovenaan) en een getal (de rij, links). "
             "Schrijf de letters bij die stippen op: samen vormen ze het wachtwoord van de schatkist.",
    "raadsel": "Raadsel {nr}",
    "kolom": "Kolom:",
    "rij": "Rij:",
    "antwoord": "Het wachtwoord van de schatkist:",
    "oplossing": "Elk raadsel geeft een kolom (letter) en een rij (getal). De stip daar draagt een letter. Samen: {antwoord}.",
    "regel": "Raadsel {nr}: kolom {kolom} ({kt}), rij {rij} ({rt}) -> {plek} -> {letter}",
    "hints": ["Los eerst alle raadsels op: schrijf per raadsel een letter en een getal op.",
              "Een plaats heet bv. C4: kolom C, rij 4. Zoek de stip daar.",
              "Veel stippen horen bij geen enkel raadsel. Negeer die."],
}


def maak_kaart(params: dict) -> dict:
    antwoord = params["antwoord"].upper()
    n, punten = len(antwoord), params["punten"]
    if not antwoord.isalpha():
        raise ValueError("Het antwoord mag enkel letters bevatten")
    if not 3 <= n <= 12:
        raise ValueError("Het antwoord moet 3 tot 12 letters hebben")
    if not n + 5 <= punten <= 70:
        raise ValueError(f"punten moet tussen {n + 5} en 70 liggen (te veel punten laat geen ruimte, te weinig is geen puzzel)")
    rng = random.Random(params["seed"])
    plekken = rng.sample([(c, r) for c in range(len(KOLOMMEN)) for r in range(RIJEN)], punten)
    letters = {}
    for i, plek in enumerate(plekken):
        letters[plek] = antwoord[i] if i < n else rng.choice(string.ascii_uppercase)
    gebruikt, raadsels = set(), []
    for i in range(n):
        teksten = []
        for bank in (KOLOM[KOLOMMEN[plekken[i][0]]], RIJ[plekken[i][1] + 1]):
            tekst = rng.choice([x for x in bank if x not in gebruikt] or bank)  # liefst geen raadsel twee keer op één blad
            gebruikt.add(tekst)
            teksten.append(tekst)
        raadsels.append({"plek": plekken[i], "letter": antwoord[i], "kolom": teksten[0], "rij": teksten[1]})
    return {"antwoord": antwoord, "letters": letters, "raadsels": raadsels}


def naam(plek: tuple[int, int]) -> str:
    return f"{KOLOMMEN[plek[0]]}{plek[1] + 1}"


def teken_kaart(p: Pdf, kaart: dict, oplossing: bool = False) -> None:
    """Raster A-J x 1-10 met een stip en letter per punt. In de oplossing: juiste stippen genummerd en met een lijn verbonden."""
    c = p.c
    breedte = len(KOLOMMEN)
    ruimte = p.y - (MARGE + 1 * cm) - 0.8 * cm
    cel = min(1.55 * cm, (W - 2 * MARGE - 0.7 * cm) / breedte, ruimte / RIJEN)
    if cel < 1.0 * cm:  # past niet meer op deze pagina
        p.pagina(TEKST["titel"] + (" - oplossing" if oplossing else ""))
        cel = min(1.55 * cm, (W - 2 * MARGE - 0.7 * cm) / breedte, (p.y - MARGE - 1.8 * cm) / RIJEN)
    x0, y0 = MARGE + 0.7 * cm, p.y - 0.7 * cm  # bovenhoek van het raster, ruimte voor de labels
    c.setStrokeGray(0.7)
    c.setLineWidth(0.5)
    for i in range(breedte + 1):
        c.line(x0 + i * cel, y0, x0 + i * cel, y0 - RIJEN * cel)
    for j in range(RIJEN + 1):
        c.line(x0, y0 - j * cel, x0 + breedte * cel, y0 - j * cel)
    c.setStrokeGray(0)
    c.setFont("Helvetica-Bold", 11)
    for i, kol in enumerate(KOLOMMEN):
        c.drawCentredString(x0 + (i + 0.5) * cel, y0 + 0.2 * cm, kol)
    for j in range(RIJEN):
        c.drawCentredString(x0 - 0.35 * cm, y0 - (j + 0.5) * cel - 4, str(j + 1))

    def midden(plek):
        return x0 + (plek[0] + 0.5) * cel, y0 - (plek[1] + 0.5) * cel

    juist = [r["plek"] for r in kaart["raadsels"]]
    if oplossing:
        c.setStrokeColorRGB(0.85, 0.15, 0.25)
        c.setLineWidth(1.5)
        for a, b in zip(juist, juist[1:]):
            c.line(*midden(a), *midden(b))
        c.setStrokeGray(0)
        c.setLineWidth(1)
    for plek, letter in kaart["letters"].items():
        x, y = midden(plek)
        c.setFillGray(0)
        c.circle(x - cel * 0.14, y - cel * 0.1, cel * 0.07, fill=1, stroke=0)
        c.setFont("Helvetica-Bold", cel * 0.34)
        c.drawString(x - cel * 0.02, y - cel * 0.2, letter)
    if oplossing:
        c.setStrokeColorRGB(0.85, 0.15, 0.25)
        c.setLineWidth(1.5)
        for i, plek in enumerate(juist, 1):
            x, y = midden(plek)
            c.circle(x, y, cel * 0.42)
            c.setFillColorRGB(0.85, 0.15, 0.25)
            c.setFont("Helvetica-Bold", 11)
            c.drawString(x - cel * 0.5, y + cel * 0.32, str(i))
        c.setStrokeGray(0)
        c.setFillGray(0)
        c.setLineWidth(1)
    p.y = y0 - RIJEN * cel - 0.4 * cm


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    kaart = maak_kaart(params)
    antwoord = kaart["antwoord"].lower()

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"], 10)
    for i, r in enumerate(kaart["raadsels"], 1):
        p.regel(f"{i}.  {t['kolom']} {r['kolom']}  {t['rij']} {r['rij']}", 10)
    teken_kaart(p, kaart)
    p.c.setFont("Helvetica-Bold", 12)
    p.c.drawString(MARGE, p.y - 4, t["antwoord"] + " " + "_" * 16)
    p.opslaan()

    regels = [t["oplossing"].format(antwoord=antwoord)]
    for i, r in enumerate(kaart["raadsels"], 1):
        regels.append(t["regel"].format(nr=i, kolom=KOLOMMEN[r["plek"][0]], kt=r["kolom"].removeprefix("De eerste letter van ").rstrip("."),
                                         rij=r["plek"][1] + 1, rt=r["rij"].rstrip("."), plek=naam(r["plek"]), letter=r["letter"]))
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, regels[:1], t["hints"], "nl")
    for regel in regels[1:]:
        b.regel(regel, 10)
    b.pagina(t["titel"] + " - oplossing")
    teken_kaart(b, kaart, oplossing=True)
    b.opslaan()
    if params.get("digitaal"):
        digitaal(kaart, uit)
    return antwoord


def digitaal(kaart: dict, uit: Path) -> None:
    """Klikbare kaart: kies een raadsel en klik op de stip die erbij hoort. De gekozen letters vormen onderaan het antwoord."""
    css = """
.kaart-raster{display:grid;gap:3px;max-width:660px;margin:0 auto}
.kop{font-family:var(--mono);font-weight:900;display:flex;align-items:center;justify-content:center;font-size:15px}
.leeg{aspect-ratio:1;border:2px solid #e3e3ea;}
.stip{aspect-ratio:1;padding:0;position:relative;border:2px solid #d8d8e4;box-shadow:none;background:#fff;display:flex;align-items:center;justify-content:center;gap:2px}
.stip:hover{background:var(--cyaan-zacht);transform:none;box-shadow:none}
.stip .punt{width:.5em;height:.5em;background:#222;display:inline-block}
.stip .let{font-family:var(--mono);font-weight:900;font-size:clamp(12px,2.6vw,20px)}
.stip.gekozen{background:var(--cyaan);border-color:var(--lijn)}
.stip.gekozen::after{content:attr(data-nr);position:absolute;top:0;left:3px;font-size:11px;font-weight:900;color:var(--magenta-donker)}
#raadsels{padding-left:0;list-style:none;display:grid;gap:10px;margin:0}
.raadsel{width:100%;text-align:left;display:flex;justify-content:space-between;gap:12px;box-shadow:none;font-weight:600}
.raadsel.actief{background:var(--zacht);border-color:var(--magenta-donker)}
.raadsel .vak{font-family:var(--mono);font-weight:900;white-space:nowrap}
"""
    body = """  <div class="kaart">
    <h2>De raadsels</h2>
    <p class="klein">Klik op een raadsel en dan op de stip. Kolom = letter, rij = getal.</p>
    <ol id="raadsels"></ol>
  </div>
  <div class="kaart"><h2>De kaart</h2><div id="kaart" class="kaart-raster"></div></div>
  <div class="kaart" id="antwoord-kaart" hidden>
    <h2>Jouw letters</h2>
    <div id="antwoord" class="antwoordbalk"></div>
  </div>"""
    gegevens = {"kolommen": KOLOMMEN, "rijen": RIJEN, "letters": {f"{c},{r}": letter for (c, r), letter in sorted(kaart["letters"].items())},  # gesorteerd: de volgorde verraadt niets
                "raadsels": [{"kolom": x["kolom"], "rij": x["rij"]} for x in kaart["raadsels"]]}
    schrijf(uit, TEKST["titel"], "Los de raadsels op en klik op de stip die erbij hoort.", body, Path(__file__).parent / "digitaal.js", gegevens, TEKST["hints"], css)


def check(params: dict) -> None:
    kaart = maak_kaart(params)
    assert len(kaart["letters"]) == params["punten"]
    plekken = [r["plek"] for r in kaart["raadsels"]]
    assert len(set(plekken)) == len(plekken)
    assert "".join(kaart["letters"][pl] for pl in plekken) == kaart["antwoord"]
    # elk raadsel hoort bij precies één kolom of rij: de teksten zijn uniek en het antwoord klopt met de plek
    teksten = [t for lijst in KOLOM.values() for t in lijst] + [t for lijst in RIJ.values() for t in lijst]
    assert len(set(teksten)) == len(teksten) and all(len(lijst) >= 2 for lijst in (*KOLOM.values(), *RIJ.values()))
    assert set(KOLOM) == set(KOLOMMEN) and set(RIJ) == set(range(1, RIJEN + 1))
    for r in kaart["raadsels"]:
        assert r["kolom"] in KOLOM[KOLOMMEN[r["plek"][0]]] and r["rij"] in RIJ[r["plek"][1] + 1]
