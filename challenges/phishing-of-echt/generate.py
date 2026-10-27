"""Phishing of echt? Berichtenkaartjes sorteren: de letters van de nepberichten, in volgorde, spellen het antwoord."""
import random
import string
from pathlib import Path

from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.utils import simpleSplit

from jr.digitaal import schrijf
from jr.pdf import MARGE, W, Pdf, begeleider

VLAGGEN = {1: "onbekende afzender", 2: "haast of dreigen", 3: "te mooi om waar te zijn",
           4: "vraagt wachtwoord of gegevens", 5: "rare link of spelling"}

# Nepberichten (phishing): kanaal, afzender, tekst, link (of None) en de rode vlaggen die erin zitten.
NEP = [
    {"kanaal": "SMS", "van": "+44 7700 900123", "link": "game-munten-gratis.win/prijs", "vlaggen": [1, 2, 3, 4, 5],
     "tekst": "Proficiat! Je wint 10.000 gratis game-munten. Klik nu en log in met je wachtwoord, anders vervalt je prijs!"},
    {"kanaal": "E-mail", "van": "Game Support <help@game-supp0rt.net>", "link": "game-supp0rt.net/login", "vlaggen": [2, 4, 5],
     "tekst": "Je account wordt binnen 24 uur verwijderd! Bevestig nu je wachtwoord via deze link."},
    {"kanaal": "E-mail", "van": "Helpdesk <info@sch00l-support.com>", "link": None, "vlaggen": [1, 4, 5],
     "tekst": "Beste leerling, je schoolwachtwoord is verlopen. Stuur het nu naar ons door, dan maken we een nieuw."},
    {"kanaal": "Chat", "van": "Sofie_2013 (ken je niet)", "link": None, "vlaggen": [1, 3, 4],
     "tekst": "Hoi! Ken je mij nog? Stuur je adres en een foto van jezelf, dan stuur ik je een cadeau!"},
    {"kanaal": "SMS", "van": "Pakketdienst", "link": "pakket-betaal.top/id83", "vlaggen": [2, 5],
     "tekst": "Je pakje kan niet bezorgd worden. Betaal vandaag nog 1,99 euro, anders gaat het terug."},
    {"kanaal": "Pop-up", "van": "Melding op je tablet", "link": "veilig-scan.apk-download.com", "vlaggen": [2, 5],
     "tekst": "WAARSCHUWING! Je tablet heeft 5 virussen! Installeer nu onze gratis app om ze te verwijderen."},
    {"kanaal": "Chat", "van": "Gamer_Pro_99 (ken je niet)", "link": None, "vlaggen": [1, 2, 3, 4],
     "tekst": "Ik geef je gratis skins als je me je inlogcode geeft. Snel, het aanbod stopt over 5 minuten!"},
    {"kanaal": "E-mail", "van": "Pretpark <win@pretpark-prijzen.xyz>", "link": "pretpark-prijzen.xyz/gratis", "vlaggen": [1, 3, 4, 5],
     "tekst": "Gewonnen: 4 gratis tickets! Deel dit bericht met 10 vrienden en vul je gegevens in."},
]
# Echte berichten: kanaal, afzender, tekst en waarom ze in orde zijn.
ECHT = [
    {"kanaal": "Chat", "van": "Mama", "link": None, "reden": "Een bekende afzender, zonder haast en zonder vraag naar gegevens.",
     "tekst": "Ik ben 10 minuutjes later. Wacht maar bij de juf, tot zo!"},
    {"kanaal": "SMS", "van": "Juf Lies", "link": None, "reden": "Een bekende afzender met een gewone mededeling.",
     "tekst": "Vergeet morgen je turnzak niet! Groetjes, juf Lies"},
    {"kanaal": "E-mail", "van": "De bibliotheek", "link": None, "reden": "Je hebt zelf een boek gereserveerd: het bericht vraagt niets.",
     "tekst": "Het boek dat je reserveerde ligt klaar. Je kan het afhalen tijdens de openingsuren."},
    {"kanaal": "Chat", "van": "Opa", "link": None, "reden": "Een bekende afzender, een lief bericht en geen vraag.",
     "tekst": "Veel plezier op je voetbalmatch! Ik kom zeker even kijken."},
    {"kanaal": "SMS", "van": "Turnclub", "link": None, "reden": "De club die jij kent, met gewone info zonder link of vraag.",
     "tekst": "De training van woensdag begint een uur later: om 18u. Tot dan!"},
]

TEKST = {
    "titel": "Phishing of echt?",
    "intro": "Sommige berichten zijn echt, andere zijn nep: iemand probeert je wachtwoord of gegevens te stelen. Dat heet phishing. Zoek de rode vlaggen, kruis de nepberichten aan en schrijf hun letters op, in de volgorde van de nummers.",
    "vlaggen": "Rode vlaggen: " + " | ".join(f"{k} {v}" for k, v in VLAGGEN.items()),
    "nep": "nep!",
    "link": "Link:",
    "antwoord": "De letters van de nepberichten:",
    "variant": "Variant {i}: {woord}",
    "oplossing": "Nepberichten zijn die met een of meer rode vlaggen. Lees de letters van de nepberichten in de volgorde van de nummers: dat spelt het antwoord.",
    "kolommen": ("Nr", "Soort", "Letter", "Waarom"),
    "echt": "echt", "phishing": "nep",
    "hints": ["Kijk eerst naar de afzender: ken je die?",
              "Vraagt het bericht je wachtwoord of gegevens, of is er haast? Dan is het nep.",
              "Een link met rare tekens of spelfouten in de naam is een rode vlag."],
}

KAART_H, KAART_B, RIJ_H = 4.0 * cm, (W - 2 * MARGE - 0.5 * cm) / 2, 4.3 * cm


def woorden(params: dict) -> list[str]:
    lijst = [w.strip().lower() for w in str(params["antwoord"]).split(",") if w.strip()]
    for w in lijst:
        if not w.isalpha():
            raise ValueError("Het antwoord mag enkel letters bevatten (meerdere woorden scheid je met een komma)")
        if not 3 <= len(w) <= len(NEP):
            raise ValueError(f"Elk antwoord moet 3 tot {len(NEP)} letters hebben (één nepbericht per letter): '{w}'")
    if not 1 <= len(lijst) <= 3:
        raise ValueError("Geef 1 tot 3 antwoorden (varianten)")
    return lijst


def maak_set(woord: str, params: dict, seed: int) -> list[dict]:
    """Willekeurige volgorde van nep- en echte kaartjes; de nepkaartjes dragen in volgorde de letters van het woord."""
    if not 1 <= params["echt"] <= len(ECHT):
        raise ValueError(f"echt moet tussen 1 en {len(ECHT)} liggen")
    rng = random.Random(seed)
    kaarten = [{**k, "nep": True} for k in rng.sample(NEP, len(woord))] + [{**k, "nep": False} for k in rng.sample(ECHT, params["echt"])]
    rng.shuffle(kaarten)
    letters = iter(woord.upper())
    for k in kaarten:
        k["letter"] = next(letters) if k["nep"] else rng.choice(string.ascii_uppercase)
    return kaarten


def teken_kaartje(c, x: float, y: float, nr: int, k: dict, t: dict) -> None:
    """Berichtkaartje met linksboven de bovenrand y: nummer, kanaal, afzender, tekst, link, nep-hokje en letter."""
    c.setStrokeGray(0.3)
    c.setLineWidth(1)
    c.roundRect(x, y - KAART_H, KAART_B, KAART_H, 6)
    c.setFillGray(0.92)
    c.rect(x + 0.5, y - 0.8 * cm, KAART_B - 1, 0.8 * cm - 0.5, fill=1, stroke=0)
    c.setFillGray(0)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x + 0.25 * cm, y - 0.55 * cm, f"{nr}")
    c.setFont("Helvetica-Bold", 8.5)
    c.drawString(x + 0.9 * cm, y - 0.5 * cm, k["kanaal"] + ":")
    c.setFont("Helvetica", 8.5)
    c.drawString(x + 0.9 * cm + stringWidth(k["kanaal"] + ": ", "Helvetica-Bold", 8.5), y - 0.5 * cm, k["van"])
    c.setFont("Helvetica", 9.5)
    for i, regel in enumerate(simpleSplit(k["tekst"], "Helvetica", 9.5, KAART_B - 0.6 * cm)):
        c.drawString(x + 0.3 * cm, y - 1.25 * cm - i * 0.38 * cm, regel)
    if k["link"]:
        c.setFillColorRGB(0.1, 0.25, 0.75)
        c.setFont("Helvetica", 9)
        c.drawString(x + 0.3 * cm, y - 2.95 * cm, f"{t['link']} {k['link']}")
        c.setFillGray(0)
    c.setLineWidth(1)
    c.rect(x + 0.3 * cm, y - 3.75 * cm, 0.45 * cm, 0.45 * cm)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(x + 0.9 * cm, y - 3.62 * cm, t["nep"])
    c.circle(x + KAART_B - 0.65 * cm, y - 3.5 * cm, 0.35 * cm)
    c.drawCentredString(x + KAART_B - 0.65 * cm, y - 3.62 * cm, k["letter"])
    c.setStrokeGray(0)


def teken_kaarten(p: Pdf, kaarten: list[dict], t: dict) -> None:
    c = p.c
    for i, k in enumerate(kaarten):
        if i % 2 == 0:
            if p.y - RIJ_H < MARGE + 2.2 * cm:
                p.pagina(t["titel"])
            if i:
                p.y -= RIJ_H
        teken_kaartje(c, MARGE + (i % 2) * (KAART_B + 0.5 * cm), p.y, i + 1, k, t)
    p.y -= RIJ_H


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    lijst = woorden(params)
    sets = [maak_set(w, params, params["seed"] + i) for i, w in enumerate(lijst)]

    for i, kaarten in enumerate(sets):
        suffix = "" if i == 0 else f"-{i + 1}"  # variant 1 houdt de standaardnaam
        p = Pdf(uit / f"deelnemer{suffix}.pdf", t["titel"])
        p.regel(t["intro"], 10)
        p.regel(t["vlaggen"], 10)
        p.ruimte(4)
        teken_kaarten(p, kaarten, t)
        p.c.setFont("Helvetica-Bold", 12)
        if p.y < MARGE + 1.5 * cm:
            p.pagina(t["titel"])
        p.c.drawString(MARGE, p.y - 6, t["antwoord"] + " " + "_ " * len(lijst[i]))
        p.opslaan()

    b = begeleider(uit / "begeleider.pdf", t["titel"], lijst[0] if len(lijst) == 1 else None, [t["oplossing"]], t["hints"], "nl")
    for i, kaarten in enumerate(sets):
        if len(lijst) > 1:
            b.kop(t["variant"].format(i=i + 1, woord=lijst[i]))
        rijen = [(str(n), t["phishing"] if k["nep"] else t["echt"], k["letter"] if k["nep"] else "-",
                  ", ".join(VLAGGEN[v] for v in k["vlaggen"]) if k["nep"] else k["reden"])
                 for n, k in enumerate(kaarten, 1)]
        b.tabel(t["kolommen"], rijen, (0.8, 1.2, 1.2, 8), 9)
    b.opslaan()
    if params.get("digitaal"):
        for i, kaarten in enumerate(sets):
            digitaal(kaarten, uit, "" if i == 0 else f"-{i + 1}", t)
    return lijst[0] if len(lijst) == 1 else "\n".join(f"variant {i + 1}: {w}" for i, w in enumerate(lijst))


def digitaal(kaarten: list[dict], uit: Path, suffix: str, t: dict) -> None:
    """Digitaal potlood: rode vlaggen aanvinken en berichten als nep markeren. Onderaan staan de letters van de berichten die jij nep noemt; de pagina controleert niets."""
    css = """
.bericht{position:relative;border:3px solid var(--lijn);margin-top:20px;background:#fff;box-shadow:6px 6px 0 var(--cyaan);overflow:hidden}
.bericht .kop{padding:8px 16px;background:#e4e4ec;font-size:16px;border-bottom:3px solid var(--lijn)}
.bericht.kanaal-sms .kop{background:var(--cyaan)}
.bericht.kanaal-chat .kop{background:#ffb3ee}
.bericht.kanaal-popup .kop{background:var(--ink);color:#fff}
.bericht .nr{font-family:var(--mono);font-weight:900;margin-right:8px}
.bericht .tekst,.bericht .link,.bericht .vlaggen,.bericht .rij{margin-left:16px;margin-right:16px}
.bericht .tekst{margin-top:14px;margin-bottom:6px;font-size:19px;max-width:44em}
.bericht .link{color:#1a3fbf;margin-top:4px;margin-bottom:4px;word-break:break-all;font-family:var(--mono);font-size:16px}
.bericht .vlaggen{display:flex;gap:8px;flex-wrap:wrap;margin-top:12px}
.bericht .rij{margin-bottom:16px}
.chip.aan{background:var(--magenta);border-color:var(--lijn)}
.bericht button.gekozen{background:var(--magenta);color:var(--ink);box-shadow:3px 3px 0 var(--ink)}
.bericht .letter{margin-left:auto;width:2.2em;height:2.2em;border:3px solid var(--lijn);display:grid;place-items:center;font-family:var(--mono);font-weight:900;font-size:20px;background:#fff}
.bericht.is-nep{background:var(--zacht)}
.bericht.is-nep::after{content:"NEP";position:absolute;right:92px;bottom:18px;transform:rotate(-10deg);border:4px solid var(--magenta-donker);color:var(--magenta-donker);font-family:var(--mono);font-weight:900;font-size:30px;padding:0 12px;opacity:.9;pointer-events:none}
@media(max-width:640px){.bericht.is-nep::after{display:none}}
"""
    gegevens = {"vlaggen": list(VLAGGEN.values()),
                "kaarten": [{"kanaal": k["kanaal"], "van": k["van"], "tekst": k["tekst"], "link": k["link"], "letter": k["letter"]} for k in kaarten]}
    body = """  <div id="kaarten"></div>
  <div class="kaart">
    <h2>Letters van de nepberichten</h2>
    <div id="woord" class="antwoordbalk"></div>
    <div class="rij"><button id="wis" type="button">Alles wissen</button></div>
  </div>"""
    schrijf(uit, t["titel"], "Is het bericht echt of nep? Zoek de rode vlaggen.", body, Path(__file__).parent / "digitaal.js", gegevens, t["hints"], css,
            naam=f"digitaal{suffix}.html")


def check(params: dict) -> None:
    lijst = woorden({**params, "antwoord": "vissen, hengel, lokaas"})
    for i, w in enumerate(lijst):
        kaarten = maak_set(w, params, params["seed"] + i)
        assert "".join(k["letter"] for k in kaarten if k["nep"]) == w.upper()
        assert sum(not k["nep"] for k in kaarten) == params["echt"]
    # elke tekst past in een kaartje: maximaal 4 regels, afzender op één regel in de kop
    for k in NEP + ECHT:
        assert len(simpleSplit(k["tekst"], "Helvetica", 9.5, KAART_B - 0.6 * cm)) <= 4, k["tekst"]
        assert stringWidth(k["kanaal"] + ": " + k["van"], "Helvetica", 8.5) < KAART_B - 1.3 * cm, k["van"]
        assert stringWidth("Link: " + (k["link"] or ""), "Helvetica", 9) < KAART_B - 0.6 * cm, k["link"]
    # elk nepbericht heeft minstens een rode vlag; ook de echte vragen nooit om gegevens of hebben een link
    assert all(k["vlaggen"] and set(k["vlaggen"]) <= set(VLAGGEN) for k in NEP)
    assert all(not k["link"] for k in ECHT)
