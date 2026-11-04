"""Hash-kraker: een gelekte lijst accounts met hashes. De deelnemers zoeken zelf uit hoe ze het wachtwoord van de beheerder vinden.

Het antwoord is het wachtwoord van de beheerder: een woord met een jaartal erachter (bv. 'voetbal2017'), gehasht met SHA-256 en een zout.
De andere vier accounts zijn de oefenronde en leren een patroon: een veelgebruikt wachtwoord, een woord, een woord met jaartal en een
andere hash met een hoofdletter. Het woord van de verkoper (Tom) is het woord van de beheerder; het jaartal is het jaar waarin de winkel begon.
"""
import csv
import hashlib
import io
import random
import re
from pathlib import Path

from jr.digitaal import schrijf
from jr.pdf import Pdf, begeleider

WOORDEN = [w for regel in (Path(__file__).parent / "woorden.txt").read_text().splitlines() if not regel.startswith("#") for w in regel.split()]
SEIZOENEN = ["zomer", "winter", "lente", "herfst"]
ZOUTTEKENS = "abcdefghjkmnpqrstuvwxyz23456789"
ANTWOORD_RE = re.compile(r"^([a-z]+)(\d{4})$")

TEKST = {
    "titel": "Hash-kraker",
    "verhaal": "Een webwinkel is gehackt: {winkel}. De aanvallers hebben de lijst met accounts gestolen, met een hash in plaats van een wachtwoord. "
               "Jullie zijn de onderzoekers die moeten aantonen hoe gevaarlijk dat is. Een hash is een vingerafdruk van een wachtwoord: je kunt hem niet "
               "omdraaien. Of toch niet?",
    "doel": "Doel: vind het wachtwoord van de beheerder en typ het in de kluis.",
    "regel": "Afspraak: enkel in deze oefenomgeving. Echte wachtwoorden of gelekte gegevens van echte mensen opzoeken of proberen, mag nooit.",
    "opdracht_laptop": "Open Hash-kraker op de laptop: je vindt er het lek, een hash-lab en een kladblok. Zoek zelf uit hoe je verder komt.",
    "opdracht": "De gelekte lijst staat in lek.csv. Zoek zelf uit hoe je het wachtwoord van de beheerder vindt.",
    "lek": "Het lek",
    "oplossing": [
        "Lek van de webwinkel {winkel}. De hashes: 32 tekens is MD5, 40 is SHA-1 en 64 is SHA-256.",
        "sofie (MD5): {sofie}, een van de meest gebruikte wachtwoorden. Je vindt het door de hash-lab met een paar veelgebruikte wachtwoorden te proberen.",
        "tom (MD5): {tom}. Het geheugensteuntje zegt: mijn favoriete sport.",
        "lotte (MD5): {lotte}. Haar steuntje zegt seizoen plus het jaar van inschrijven (zie de kolom aangemaakt).",
        "jan (SHA-1): {jan}. Het steuntje zegt: begroeting met hoofdletter en 01. Hoofdletters tellen mee in de hash.",
        "beheerder (SHA-256 met zout '{zout}'): {antwoord}. Het steuntje zegt: zoals Tom, maar met het jaar waarin de winkel begon (zie aangemaakt). "
        "Het zout staat ervoor: hash '{zout}{antwoord}', niet enkel '{antwoord}'. Zonder dat zout geeft de hash een heel andere uitkomst.",
        "Antwoord: {antwoord}.",
    ],
    "hints": [
        "Een hash is een vingerafdruk van een wachtwoord: je kunt hem niet omdraaien. Maar je kunt wel zelf wachtwoorden hashen en kijken of de vingerafdruk gelijk is.",
        "Tel de tekens van een hash: 32 is MD5, 40 is SHA-1, 64 is SHA-256. De hash-lab rekent ze alle drie uit en vergelijkt met het lek. Begin met de geheugensteuntjes.",
        "Mensen gebruiken eenvoudige patronen: een woord, een jaartal, een hoofdletter, '01'. Kijk ook naar de kolom aangemaakt.",
        "De beheerder heeft een zout. Dat is een stukje tekst dat voor het wachtwoord gezet wordt voordat er gehasht wordt. Probeer zout en wachtwoord als één tekst.",
        "Veel wachtwoorden proberen? Schrijf code in het kladblok: WOORDEN is een lijst woorden en md5(), sha1() en sha256() rekenen hashes uit.",
    ],
}

KLADBLOK = """// Schrijf hier je eigen code. Beschikbaar: md5(tekst), sha1(tekst), sha256(tekst) en LEK (de lijst met accounts).
// Voorbeeld: kijk of een van deze pogingen bij de eerste account past.
const doel = LEK[0].hash;
console.log(LEK[0].gebruiker, doel);
for (const poging of ["abc", "hallo", "wachtwoord"]) {
  if (md5(poging) === doel) console.log("Gevonden:", poging);
}
"""


def hashers() -> dict:
    return {"md5": lambda s: hashlib.md5(s.encode()).hexdigest(), "sha1": lambda s: hashlib.sha1(s.encode()).hexdigest(),
            "sha256": lambda s: hashlib.sha256(s.encode()).hexdigest()}


def maak_lek(antwoord: str, seed: int) -> tuple[list[dict], dict[str, str]]:
    """De accounts (met hash) en de wachtwoorden daarachter, per gebruiker."""
    m = ANTWOORD_RE.match(antwoord)
    if not m:
        raise ValueError("antwoord moet een woord in kleine letters met een jaartal van 4 cijfers zijn, bv. 'voetbal2017'")
    woord, jaar = m.group(1), m.group(2)
    rng = random.Random(seed)
    h = hashers()
    start = int(jaar) + 1  # alle klanten schreven zich in nadat de winkel opende
    seizoen, lotte_jaar = rng.choice(SEIZOENEN), rng.randint(start, start + 5)
    zout = "".join(rng.choice(ZOUTTEKENS) for _ in range(4))
    ww = {"sofie": "123456", "tom": woord, "lotte": f"{seizoen}{lotte_jaar}", "jan": "Welkom01", "beheerder": antwoord}

    def datum(j: int) -> str:
        return f"{j}-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}"

    rijen = [
        {"gebruiker": "sofie", "email": "sofie.d@mail.example", "hash": h["md5"](ww["sofie"]), "zout": "", "aangemaakt": datum(rng.randint(start, start + 5)),
         "steun": "makkelijk te onthouden: de eerste zes cijfers"},
        {"gebruiker": "tom", "email": "tom@sporthoek.example", "hash": h["md5"](ww["tom"]), "zout": "", "aangemaakt": datum(int(jaar) + 1),
         "steun": "mijn favoriete sport"},
        {"gebruiker": "lotte", "email": "lotte.v@mail.example", "hash": h["md5"](ww["lotte"]), "zout": "", "aangemaakt": datum(lotte_jaar),
         "steun": "mijn lievelingsseizoen en het jaar waarin ik me inschreef"},
        {"gebruiker": "jan", "email": "jan_peeters@mail.example", "hash": h["sha1"](ww["jan"]), "zout": "", "aangemaakt": datum(rng.randint(start, start + 5)),
         "steun": "wat je zegt tegen iemand die binnenkomt, met hoofdletter, en 01"},
        {"gebruiker": "beheerder", "email": "beheer@sporthoek.example", "hash": h["sha256"](zout + ww["beheerder"]), "zout": zout,
         "aangemaakt": datum(int(jaar)), "steun": "zoals Tom, maar met het jaar waarin ik de winkel opende", "beheerder": True},
    ]
    return rijen, ww


def lek_csv(rijen: list[dict]) -> str:
    uit = io.StringIO()
    w = csv.writer(uit, lineterminator="\n")
    w.writerow(["gebruiker", "email", "hash", "zout", "aangemaakt", "geheugensteuntje"])
    for r in rijen:
        w.writerow([r["gebruiker"], r["email"], r["hash"], r["zout"], r["aangemaakt"], r["steun"]])
    return uit.getvalue()


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    antwoord = params["antwoord"].strip().lower()
    rijen, ww = maak_lek(antwoord, params["seed"])
    winkel = params["winkel"]
    csv_tekst = lek_csv(rijen)
    (uit / "lek.csv").write_text(csv_tekst)

    if params.get("digitaal"):
        body = """  <div class="kaart">
    <h2>Het lek</h2>
    <div style="overflow-x:auto"><table class="lek">
      <thead><tr><th>Gebruiker</th><th>E-mail</th><th>Hash</th><th>Zout</th><th>Aangemaakt</th><th>Geheugensteuntje</th><th>Gekraakt</th></tr></thead>
      <tbody id="lek-lijf"></tbody>
    </table></div>
    <div class="rij"><strong id="teller"></strong><button id="wis-lek" type="button" class="chip">Wis wat gekraakt is</button></div>
    <div id="beheerder-klaar" hidden><p>De beheerder is gekraakt. Typ dit wachtwoord in de kluis:</p><div class="antwoordbalk" id="beheerder-ww"></div></div>
  </div>
  <div class="kaart">
    <h2>Hash-lab</h2>
    <label for="poging">Probeer een wachtwoord (of een tekst)</label>
    <div class="rij" style="margin-top:6px"><input type="text" id="poging" autocomplete="off" spellcheck="false" autocapitalize="off"></div>
    <div id="uitvoer"></div>
    <div class="melding" id="uitslag"></div>
    <p class="klein">De hash-lab vergelijkt elke hash meteen met het lek. Hoofdletters en spaties tellen mee.</p>
  </div>"""
        css = """
table.lek{border-collapse:collapse;width:100%;font-size:14px}
table.lek th,table.lek td{border:2px solid var(--lijn);padding:6px 8px;text-align:left;vertical-align:top}
table.lek th{background:var(--ink);color:#fff;font-family:var(--mono);font-size:13px}
table.lek td.hash{font-family:var(--mono);font-size:12px;word-break:break-all;min-width:14em}
table.lek tr.gekraakt td{background:var(--cyaan-zacht)}
.hashrij{display:flex;gap:10px;align-items:baseline;flex-wrap:wrap;padding:6px 8px;border:2px solid transparent;margin-top:6px}
.hashrij .algo{font-weight:700;min-width:11em}
.hashrij code{font-family:var(--mono);font-size:13px;word-break:break-all}
.hashrij.raak{background:var(--cyaan-zacht);border-color:var(--lijn)}
"""
        schrijf(uit, t["titel"], t["verhaal"].format(winkel=winkel), body, Path(__file__).parent / "digitaal.js",
                {"lek": rijen, "woorden": WOORDEN}, t["hints"], css=css, kladblok=KLADBLOK)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["verhaal"].format(winkel=winkel))
    p.regel(t["doel"])
    p.regel(t["regel"])
    p.regel(t["opdracht_laptop" if params.get("digitaal") else "opdracht"])
    p.kop(t["lek"])
    p.mono(csv_tekst, 7)
    p.opslaan()

    oplossing = [x.format(winkel=winkel, antwoord=antwoord, zout=rijen[4]["zout"], sofie=ww["sofie"], tom=ww["tom"], lotte=ww["lotte"], jan=ww["jan"])
                 for x in t["oplossing"]]
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, oplossing, t["hints"], params["taal"])
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    """Hashes kloppen met de wachtwoorden en elk wachtwoord is te vinden met de aanpak uit de hints (woordenlijst plus patronen)."""
    antwoord = params["antwoord"].strip().lower()
    rijen, ww = maak_lek(antwoord, params["seed"])
    h = hashers()
    lengte = {32: "md5", 40: "sha1", 64: "sha256"}
    for r in rijen:
        assert len(r["hash"]) in lengte, f"{r['gebruiker']}: onbekende hashlengte"
    assert rijen[4]["zout"] and len(rijen[4]["hash"]) == 64
    assert h["sha256"](rijen[4]["zout"] + antwoord) == rijen[4]["hash"]
    assert h["sha256"](antwoord) != rijen[4]["hash"], "zonder zout mag de hash niet kloppen"
    assert antwoord == ww["tom"] + antwoord[-4:] and antwoord[:-4] in WOORDEN, "het woord van het antwoord moet in de woordenlijst staan"
    # simuleer wat een deelnemer met code doet: elk woord, met jaartallen en variaties, tegen elke hash
    kandidaten = set()
    for w in WOORDEN:
        for v in (w, w.capitalize(), w.upper()):
            kandidaten.add(v)
            for j in range(1990, 2031):
                kandidaten.add(f"{v}{j}")
            kandidaten.add(f"{v}01")
    gevonden = {}
    for r in rijen:
        for k in kandidaten:
            invoer = r["zout"] + k if r["zout"] else k
            if h[lengte[len(r["hash"])]](invoer) == r["hash"]:
                gevonden[r["gebruiker"]] = k
    assert gevonden == ww, f"niet alles te vinden met woorden en patronen: gevonden {gevonden}, verwacht {ww}"
