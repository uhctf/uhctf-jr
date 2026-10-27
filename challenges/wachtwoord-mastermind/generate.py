"""Wachtwoord-mastermind: raad het wachtwoord uit het profiel, met feedback per vak van een begeleider."""
import random
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, W, Pdf, begeleider

LETTERS = "ABCDEFGHIJ"

# categorie -> (label nl, label en, mogelijke waarden). Waarden zijn kleine letters of cijfers, zonder spaties.
CATEGORIEEN = {
    "huisdier": ("Huisdier", "Pet", ["rex", "mimi", "bobbie", "luna", "pluto", "kiwi"]),
    "jaar": ("Geboortejaar", "Birth year", ["2013", "2014", "2015"]),
    "eten": ("Lievelingseten", "Favourite food", ["pizza", "friet", "pasta", "pannenkoek", "sushi"]),
    "hobby": ("Hobby", "Hobby", ["voetbal", "dansen", "tekenen", "zwemmen", "gamen", "judo"]),
    "kleur": ("Lievelingskleur", "Favourite colour", ["blauw", "groen", "rood", "paars", "geel", "roze"]),
    "getal": ("Lievelingsgetal", "Favourite number", ["7", "10", "13", "21", "42"]),
    "vriend": ("Beste vriend(in)", "Best friend", ["sam", "noor", "milan", "emma", "jules", "lien"]),
    "spel": ("Lievelingsspel", "Favourite game", ["minecraft", "mario", "fifa", "tetris", "zelda"]),
}
KLEUREN = [(0.16, 0.45, 0.85), (0.55, 0.25, 0.75), (0.85, 0.3, 0.45), (0.1, 0.6, 0.5), (0.9, 0.5, 0.15)]
NAMEN = ["Lotte", "Yasmine", "Finn", "Arne", "Elise", "Jonas", "Maya", "Lars"]

TEKST = {
    "nl": {
        "titel": "Wachtwoord-mastermind",
        "intro": "{naam} is het wachtwoord vergeten. Het bestaat uit {n} dingen uit het profiel (het andere blad), in een bepaalde volgorde.",
        "regels": ["Schrijf {n} letters uit het profiel in een rij.",
                   "De begeleider zegt per vak: juist, fout of verkeerde plaats. Markeer dat met het juiste rondje.",
                   "Het wachtwoord is de {n} dingen aan elkaar, in kleine letters."],
        "voorbeeld": "Voorbeeld (grijze rij): het wachtwoord is {geheim}, je gokt {gok}.",
        "soort": {"juist": "juist", "fout": "fout", "plaats": "juist maar verkeerde plaats"},
        "variant": "Variant {i}: {naam}",
        "profiel": "Profiel van {naam}", "bio": "Hoi! Dit is mijn profiel. Volg me!",
        "gok": "Gok", "legenda": "juist", "legenda2": "fout", "legenda3": "juist, verkeerde plaats",
        "oplossing": "Het wachtwoord van {naam} is, in volgorde, {letters}: {delen}. Aan elkaar geplakt: {antwoord}. (seed {seed}: zet seed = {seed} bij de opties van deze uitdaging om hetzelfde profiel opnieuw te bouwen)",
        "controle": "Controle van een gok, per letter: staat de letter op die plaats in het wachtwoord, zeg dan juist. Zit hij wel in het wachtwoord maar op een andere plaats, zeg dan juist maar verkeerde plaats. "
                    "Zit hij er niet in, zeg dan fout. Een kind markeert dat in het vak.",
        "hints": ["Alle {n} delen van het wachtwoord staan in het profiel.",
                  "Begin met een gok en gebruik de feedback: wat staat goed, wat niet?",
                  "Sluit dingen uit: een letter die fout is, zit niet in het wachtwoord."],
    },
    "en": {
        "titel": "Password mastermind",
        "intro": "{naam} forgot the password. It consists of {n} things from the profile (the other sheet), in a certain order.",
        "regels": ["Write {n} letters from the profile in a row.",
                   "The facilitator says for each box: right, wrong or wrong place. Mark it with the matching circle.",
                   "The password is the {n} things glued together, in lower case."],
        "voorbeeld": "Example (grey row): the password is {geheim}, you guess {gok}.",
        "soort": {"juist": "right", "fout": "wrong", "plaats": "right but wrong place"},
        "variant": "Variant {i}: {naam}",
        "profiel": "{naam}'s profile", "bio": "Hi! This is my profile. Follow me!",
        "gok": "Guess", "legenda": "right", "legenda2": "wrong", "legenda3": "right, wrong place",
        "oplossing": "{naam}'s password is, in order, {letters}: {delen}. Glued together: {antwoord}. (seed {seed}: set seed = {seed} in this challenge's options to rebuild the same profile)",
        "controle": "Checking a guess, per letter: if the letter is at that position in the password, say right. If it is in the password but at another position, say right but wrong place. "
                    "If it is not in the password, say wrong. The child marks that in the box.",
        "hints": ["All {n} parts of the password are in the profile.",
                  "Start with a guess and use the feedback: what is right, what is not?",
                  "Rule things out: a letter that is wrong is not in the password."],
    },
}


README_ANTWOORD = "(willekeurig, elke bouw een ander profiel)"  # voor de README, zie tools/jr/readme.py


def los_seed(params: dict) -> dict:
    """seed = 0 betekent een willekeurig profiel: kies hier eenmalig een seed, zodat alles in een bouw klopt."""
    if params["seed"] == 0:
        return {**params, "seed": random.SystemRandom().randrange(1, 10**6)}
    return params


def maak_profiel(params: dict, taboe: tuple = ()) -> dict:
    n, aantal = params["lengte"], params["aantal"]
    if not 1 <= params["pogingen"] <= 10:
        raise ValueError("pogingen moet tussen 1 en 10 liggen (meer rijen passen niet op de pagina)")
    if not 1 <= params["varianten"] <= len(NAMEN):
        raise ValueError(f"varianten moet tussen 1 en {len(NAMEN)} liggen (elke variant krijgt een andere naam)")
    if not 2 <= n <= aantal <= min(len(CATEGORIEEN), len(LETTERS)):
        raise ValueError(f"Kies 2 <= lengte <= aantal <= {min(len(CATEGORIEEN), len(LETTERS))}")
    rng = random.Random(params["seed"])
    cats = rng.sample(list(CATEGORIEEN), aantal)  # volgorde in het profiel = volgorde van de letters
    waarden = {c: rng.choice(CATEGORIEEN[c][2]) for c in cats}
    geheim = rng.sample(range(aantal), n)  # indexen in het profiel, in wachtwoordvolgorde
    return {"naam": rng.choice([x for x in NAMEN if x not in taboe]), "cats": cats, "waarden": waarden, "geheim": geheim,
            "wachtwoord": "".join(waarden[cats[i]] for i in geheim)}


def feedback(geheim: list[int], gok: list[int]) -> list[str]:
    """Per vak: 'juist' (juiste plaats), 'plaats' (zit erin, andere plaats) of 'fout' (zit er niet in)."""
    return ["juist" if g == h else "plaats" if g in geheim else "fout" for g, h in zip(gok, geheim)]


def vinkje(c, x: float, y: float, r: float, soort: str) -> None:
    """Rondje om aan te kruisen: vinkje (juist), kruisje (fout) of pijltje heen en weer (juist, verkeerde plaats)."""
    c.setLineWidth(0.8)
    c.circle(x, y, r)
    c.setLineWidth(1.2)
    if soort == "juist":
        c.lines([(x - r * 0.5, y, x - r * 0.1, y - r * 0.45), (x - r * 0.1, y - r * 0.45, x + r * 0.55, y + r * 0.5)])
    elif soort == "fout":
        c.lines([(x - r * 0.4, y - r * 0.4, x + r * 0.4, y + r * 0.4), (x - r * 0.4, y + r * 0.4, x + r * 0.4, y - r * 0.4)])
    else:
        k = r * 0.2
        c.lines([(x - r * 0.55, y, x + r * 0.55, y),
                 (x - r * 0.55, y, x - r * 0.25, y + k), (x - r * 0.55, y, x - r * 0.25, y - k),
                 (x + r * 0.55, y, x + r * 0.25, y + k), (x + r * 0.55, y, x + r * 0.25, y - k)])
    c.setLineWidth(1)


SOORTEN = ("juist", "fout", "plaats")


def voorbeeld(n: int, aantal: int) -> tuple[list[int], list[int]]:
    """Voorbeeldgok bij een verzonnen wachtwoord: een juiste plek, twee verwisselde en (als er afleiders zijn) een foute."""
    geheim = list(range(n))
    gok = geheim[:]
    if n >= 3:
        gok[1], gok[2] = gok[2], gok[1]
    if aantal > n:
        gok[-1] = n
    return geheim, gok


def teken_schema(p: Pdf, n: int, aantal: int, pogingen: int, t: dict) -> None:
    """Lijst met gokken. In elk vak schrijf je een letter en markeer je het als juist, fout of juist maar verkeerde plaats."""
    c = p.c
    gat = 0.15 * cm
    x_vak = MARGE + 0.9 * cm
    vak_b = (W - MARGE - x_vak - (n - 1) * gat) / n
    vak_h, rij_h = 1.8 * cm, 2.2 * cm
    geheim, gok = voorbeeld(n, aantal)
    # het voorbeeld (een extra rij) komt er enkel bij als het op de pagina past
    met_voorbeeld = p.y - 3 * 10 * 1.4 - 4 - 0.3 * cm - (pogingen + 1) * rij_h > MARGE + 1 * cm
    if met_voorbeeld:
        p.regel(t["voorbeeld"].format(geheim=" ".join(LETTERS[i] for i in geheim), gok=" ".join(LETTERS[i] for i in gok)), 10)
    p.ruimte(4)
    kop_y = p.y - 0.3 * cm
    c.setFont("Helvetica-Bold", 9)
    c.drawString(MARGE, kop_y, t["gok"])
    # legenda: wat betekent welk rondje
    x = x_vak + 1.6 * cm
    for soort, label in zip(SOORTEN, (t["legenda"], t["legenda2"], t["legenda3"])):
        vinkje(c, x, kop_y + 3, 0.19 * cm, soort)
        c.setFont("Helvetica", 9)
        c.drawString(x + 0.35 * cm, kop_y, label)
        x += 0.7 * cm + c.stringWidth(label, "Helvetica", 9) + 0.5 * cm

    def rij(y: float, label: str, letters: list[int] | None = None) -> None:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGE, y + rij_h / 2 - 0.1 * cm, label)
        gekozen = feedback(geheim, letters) if letters else []
        for k in range(n):
            x = x_vak + k * (vak_b + gat)
            c.setLineWidth(1)
            if letters:  # voorbeeldrij: grijs, met letter en de juiste markering aangeduid
                c.setFillGray(0.9)
                c.roundRect(x, y + 0.1 * cm, vak_b, vak_h, 4, fill=1)
                c.setFillGray(0)
                c.setFont("Helvetica-Bold", 20)
                c.drawCentredString(x + vak_b / 2, y + 0.1 * cm + 1.1 * cm, LETTERS[letters[k]])
            else:
                c.roundRect(x, y + 0.1 * cm, vak_b, vak_h, 4)
            for i, soort in enumerate(SOORTEN):
                cx, cy = x + vak_b * (0.25 + 0.25 * i), y + 0.1 * cm + 0.4 * cm
                if letters and soort == gekozen[k]:
                    c.setFillGray(0.6)
                    c.circle(cx, cy, 0.22 * cm, fill=1, stroke=0)
                    c.setFillGray(0)
                vinkje(c, cx, cy, 0.22 * cm, soort)

    rijen = 0
    if met_voorbeeld:
        rij(kop_y - 0.3 * cm - rij_h, "bv.", gok)
        rijen = 1
    for g in range(pogingen):
        rij(kop_y - 0.3 * cm - (g + 1 + rijen) * rij_h, str(g + 1))
    p.y = kop_y - 0.3 * cm - (pogingen + rijen) * rij_h


def teken_profiel(p: Pdf, pr: dict, t: dict, taalnr: int, seed: int) -> None:
    """Profielkaart zoals op sociale media: banner, avatar, naam, bio en de gegevens als lijst."""
    c = p.c
    rng = random.Random(f"profiel-{seed}")  # los van de wachtwoord-rng, zodat het antwoord niet verandert
    kleur = rng.choice(KLEUREN)
    naam, cats = pr["naam"], pr["cats"]
    b = W - 2 * MARGE
    top = p.y
    banner_h = 3.6 * cm
    body_h = 4.9 * cm + len(cats) * 1.25 * cm  # onder de banner
    c.saveState()
    pad = c.beginPath()
    pad.roundRect(MARGE, top - banner_h - body_h, b, banner_h + body_h, 14)
    c.clipPath(pad, stroke=0, fill=0)
    c.setFillColorRGB(*kleur)
    c.rect(MARGE, top - banner_h, b, banner_h, fill=1, stroke=0)
    c.setFillColorRGB(1, 1, 1)
    c.setFillAlpha(0.15)
    for i in range(7):  # decoratieve cirkels in de banner
        c.circle(MARGE + (i * 3.1 + rng.random()) * cm, top - banner_h * (0.2 + 0.6 * rng.random()), (0.4 + rng.random()) * cm, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.setFillColorRGB(0.97, 0.97, 0.98)
    c.rect(MARGE, top - banner_h - body_h, b, body_h, fill=1, stroke=0)
    c.restoreState()
    c.setLineWidth(1)
    c.setStrokeGray(0.8)
    c.roundRect(MARGE, top - banner_h - body_h, b, banner_h + body_h, 14)
    c.setStrokeGray(0)

    # avatar over de rand van de banner
    ax, ay, ar = MARGE + 2.6 * cm, top - banner_h, 1.7 * cm
    c.setFillGray(1)
    c.circle(ax, ay, ar + 0.15 * cm, fill=1, stroke=0)
    c.setFillColorRGB(*kleur)
    c.circle(ax, ay, ar, fill=1, stroke=0)
    c.setFillGray(1)
    c.setFont("Helvetica-Bold", 44)
    c.drawCentredString(ax, ay - 15, naam[0])
    c.setFillGray(0)
    y = ay - ar - 0.9 * cm
    c.setFont("Helvetica-Bold", 22)
    c.drawString(MARGE + 0.9 * cm, y, naam)
    c.setFont("Helvetica", 11)
    c.setFillGray(0.4)
    c.drawString(MARGE + 0.9 * cm, y - 0.6 * cm, f"@{naam.lower()}_online")
    c.setFillGray(0)
    c.setFont("Helvetica", 12)
    c.drawString(MARGE + 0.9 * cm, y - 1.4 * cm, t["bio"])

    # gegevens: elke rij een kaartje met letterbadge, label en waarde
    y -= 2.3 * cm
    rij_h, vak_h = 1.25 * cm, 1.0 * cm
    for i, cat in enumerate(cats):
        yy = y - i * rij_h - vak_h
        c.setFillGray(1)
        c.setStrokeGray(0.85)
        c.roundRect(MARGE + 0.7 * cm, yy, b - 1.4 * cm, vak_h, 8, fill=1)
        c.setFillColorRGB(*kleur)
        c.circle(MARGE + 1.5 * cm, yy + vak_h / 2, 0.36 * cm, fill=1, stroke=0)
        c.setFillGray(1)
        c.setFont("Helvetica-Bold", 12)
        c.drawCentredString(MARGE + 1.5 * cm, yy + vak_h / 2 - 4.2, LETTERS[i])
        c.setFillGray(0.45)
        c.setFont("Helvetica", 10)
        c.drawString(MARGE + 2.3 * cm, yy + vak_h / 2 - 3.5, CATEGORIEEN[cat][taalnr])
        c.setFillGray(0)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(MARGE + 7.2 * cm, yy + vak_h / 2 - 5, pr["waarden"][cat])
    c.setStrokeGray(0)
    p.opslaan()


def antwoord_van(params: dict) -> str:
    return maak_profiel(params)["wachtwoord"]


def maak_varianten(params: dict) -> list[tuple[dict, dict]]:
    """Per variant (parameters, profiel); variant i gebruikt seed + i en een eigen naam."""
    resultaat, namen = [], ()
    for i in range(params["varianten"]):
        pi = {**params, "seed": params["seed"] + i}
        pr = maak_profiel(pi, namen)
        namen += (pr["naam"],)
        resultaat.append((pi, pr))
    return resultaat


def digitaal_varianten(items: list, params: dict, taalnr: int, uit: Path, hints: list[str]) -> None:
    """Spelbare versie per variant (digitaal.html, digitaal-2.html, ...): de pagina geeft de feedback per vak, zoals de begeleider op papier, maar zegt nooit of je het wachtwoord gevonden hebt."""
    css = """
.profiel-raster{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));gap:12px}
.item{display:grid;grid-template-columns:46px 1fr;grid-template-rows:auto auto;gap:0 12px;text-align:left;align-items:center;padding:10px 12px}
.item .badge{grid-row:1 / span 2;width:46px;height:46px;background:var(--cyaan);border:3px solid var(--lijn);font-family:var(--mono);font-size:22px;font-weight:900;display:grid;place-items:center}
.item:nth-child(even) .badge{background:var(--magenta)}
.item .label{font-size:13px;color:var(--muted);font-weight:600}
.item .waarde{font-size:20px}
.gokrij{display:flex;gap:10px;margin:10px 0;align-items:stretch}
.gokrij .nr{width:1.6em;display:flex;align-items:center;font-family:var(--mono);font-weight:900;font-size:20px}
.vakje{flex:1;min-width:0;min-height:76px;display:flex;flex-direction:column;align-items:center;justify-content:center;border:3px solid var(--lijn);padding:4px;font-family:var(--mono);font-size:28px;font-weight:900;background:#fff}
button.vakje{box-shadow:none}
.vakje.leeg:not(.gevuld){border-style:dashed;color:var(--muted);font-weight:400}
.vakje.gevuld{background:var(--zacht)}
.vakje .klein{font-family:system-ui,sans-serif;font-size:12px;font-weight:700;text-align:center;color:var(--ink)}
.vakje.juist{background:var(--cyaan)}
.vakje.fout{background:#e4e4ec;color:var(--muted)}
.vakje.plaats{background:#ffb3ee}
"""
    for i, (pi, pr) in enumerate(items):
        suffix = "" if i == 0 else f"-{i + 1}"
        gegevens = {"lengte": params["lengte"], "geheim": pr["geheim"],
                    "items": [{"letter": LETTERS[j], "label": CATEGORIEEN[cat][taalnr], "waarde": pr["waarden"][cat]}
                              for j, cat in enumerate(pr["cats"])]}
        body = """  <div class="kaart">
    <h2>Het profiel van """ + pr["naam"] + """</h2>
    <div id="profiel" class="profiel-raster"></div>
  </div>
  <div class="kaart">
    <h2>Jouw gokken</h2>
    <div id="historiek"></div>
    <div id="nu" class="gokrij" style="margin-top:12px"></div>
    <div class="rij"><button id="gok" class="primair" type="button">Gok!</button><button id="wis" type="button">Wis mijn gok</button><button id="opnieuw" type="button">Opnieuw beginnen</button></div>
    <p>Als wachtwoord: <span id="tekst-gok" class="antwoordbalk"></span></p>
  </div>
  </div>"""
        schrijf(uit, TEKST["nl"]["titel"], f"{pr['naam']} is het wachtwoord vergeten. Het bestaat uit {params['lengte']} dingen uit het profiel, in een bepaalde volgorde.",
                body, Path(__file__).parent / "digitaal.js", gegevens, hints, css, naam=f"digitaal{suffix}.html")


def generate(params: dict, uit: Path) -> str:
    params = los_seed(params)
    t = TEKST.get(params["taal"], TEKST["nl"])
    taalnr = 1 if params["taal"] == "en" else 0  # kolom in CATEGORIEEN
    n = params["lengte"]
    items = maak_varianten(params)

    oplossing, antwoorden = [], []
    for i, (pi, pr) in enumerate(items):
        naam, cats = pr["naam"], pr["cats"]
        suffix = "" if i == 0 else f"-{i + 1}"  # variant 1 houdt de standaardnamen
        teken_profiel(Pdf(uit / f"profiel{suffix}.pdf", t["profiel"].format(naam=naam)), pr, t, taalnr, pi["seed"])

        p = Pdf(uit / f"deelnemer{suffix}.pdf", t["titel"])
        p.regel(t["intro"].format(naam=naam, n=n))
        for r in t["regels"]:
            p.regel("- " + r.format(n=n), 10)
        teken_schema(p, n, params["aantal"], params["pogingen"], t)
        p.opslaan()

        letters = " ".join(LETTERS[j] for j in pr["geheim"])
        delen = " + ".join(pr["waarden"][cats[j]] for j in pr["geheim"])
        tekst = t["oplossing"].format(naam=naam, letters=letters, delen=delen, antwoord=pr["wachtwoord"], seed=pi["seed"])
        if len(items) > 1:
            tekst = t["variant"].format(i=i + 1, naam=naam) + ". " + tekst
        oplossing.append(tekst)
        antwoorden.append(pr["wachtwoord"] if len(items) == 1 else f"{naam}: {pr['wachtwoord']}")

    antwoord = "\n".join(antwoorden)
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoorden[0] if len(items) == 1 else None, oplossing + [t["controle"]],
                   [h.format(n=n) for h in t["hints"]], params["taal"])
    b.opslaan()
    if params.get("digitaal"):
        digitaal_varianten(items, params, taalnr, uit, [h.format(n=n) for h in t["hints"]])
    return antwoord


def check(params: dict) -> None:
    params = los_seed(params)
    pr = maak_profiel(params)
    n = params["lengte"]
    assert len(set(pr["geheim"])) == n and len(pr["geheim"]) == n
    assert feedback(pr["geheim"], pr["geheim"]) == ["juist"] * n
    assert feedback([0, 1, 2], [2, 1, 3]) == ["plaats", "juist", "fout"]
    assert antwoord_van(params) == pr["wachtwoord"]
    assert pr["wachtwoord"].isalnum() and pr["wachtwoord"] == pr["wachtwoord"].lower()
    # elk profielonderdeel is uniek bruikbaar: geen twee categorieen met dezelfde waarde
    assert len(set(pr["waarden"].values())) == len(pr["waarden"])
    # variants: eigen naam per variant, en het voorbeeld toont juist, fout en verkeerde plaats
    namen = [v[1]["naam"] for v in maak_varianten({**params, "varianten": 3})]
    assert len(set(namen)) == 3
    geheim, gok = voorbeeld(n, params["aantal"])
    assert set(feedback(geheim, gok)) == {"juist", "plaats", "fout"} or n < 3
