"""Wachtwoord-mastermind: raad het wachtwoord uit het profiel, met feedback per vak van een begeleider."""
import random
from pathlib import Path

from reportlab.lib.units import cm

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
        "intro": "{naam} is het wachtwoord vergeten! Het enige wat {naam} nog weet: er zitten {n} favoriete dingen uit het profiel in (zie het andere blad), in een bepaalde volgorde. Kun jij helpen om het wachtwoord terug te vinden?",
        "regels": ["Schrijf {n} letters uit het profiel in een rij.",
                   "De begeleider zegt per vak of het juist is, fout, of juist maar op de verkeerde plaats. Markeer dat met het juiste rondje.",
                   "Het wachtwoord is de {n} dingen aan elkaar, in kleine letters."],
        "profiel": "Profiel van {naam}", "bio": "Hoi! Dit is mijn profiel. Volg me!",
        "gok": "Gok", "legenda": "juist", "legenda2": "fout", "legenda3": "juist, verkeerde plaats",
        "oplossing": "Het wachtwoord van {naam} is, in volgorde, {letters}: {delen}. Aan elkaar geplakt: {antwoord}. (seed {seed}: bouw opnieuw met --set seed={seed} voor hetzelfde profiel)",
        "controle": "Controle van een gok, per letter: staat de letter op die plaats in het wachtwoord, zeg dan juist. Zit hij wel in het wachtwoord maar op een andere plaats, zeg dan juist maar verkeerde plaats. "
                    "Zit hij er niet in, zeg dan fout. Een kind markeert dat in het vak.",
        "hints": ["Alle {n} delen van het wachtwoord staan in het profiel.",
                  "Begin met een gok en gebruik de feedback: wat staat goed, wat niet?",
                  "Sluit dingen uit: een letter die fout is, zit niet in het wachtwoord."],
    },
    "en": {
        "titel": "Password mastermind",
        "intro": "{naam} forgot the password! All {naam} still remembers is that it contains {n} favourite things from the profile (see the other sheet), in a certain order. Can you help find the password?",
        "regels": ["Write {n} letters from the profile in a row.",
                   "The facilitator says for each box whether it is right, wrong, or right but in the wrong place. Mark it with the matching circle.",
                   "The password is the {n} things glued together, in lower case."],
        "profiel": "{naam}'s profile", "bio": "Hi! This is my profile. Follow me!",
        "gok": "Guess", "legenda": "right", "legenda2": "wrong", "legenda3": "right, wrong place",
        "oplossing": "{naam}'s password is, in order, {letters}: {delen}. Glued together: {antwoord}. (seed {seed}: rebuild with --set seed={seed} for the same profile)",
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


def maak_profiel(params: dict) -> dict:
    n, aantal = params["lengte"], params["aantal"]
    if not 1 <= params["pogingen"] <= 10:
        raise ValueError("pogingen moet tussen 1 en 10 liggen (meer rijen passen niet op de pagina)")
    if not 2 <= n <= aantal <= min(len(CATEGORIEEN), len(LETTERS)):
        raise ValueError(f"Kies 2 <= lengte <= aantal <= {min(len(CATEGORIEEN), len(LETTERS))}")
    rng = random.Random(params["seed"])
    cats = rng.sample(list(CATEGORIEEN), aantal)  # volgorde in het profiel = volgorde van de letters
    waarden = {c: rng.choice(CATEGORIEEN[c][2]) for c in cats}
    geheim = rng.sample(range(aantal), n)  # indexen in het profiel, in wachtwoordvolgorde
    return {"naam": rng.choice(NAMEN), "cats": cats, "waarden": waarden, "geheim": geheim,
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


def teken_schema(p: Pdf, n: int, pogingen: int, t: dict) -> None:
    """Lijst met gokken. In elk vak schrijf je een letter en markeer je het als juist, fout of juist maar verkeerde plaats."""
    c = p.c
    gat = 0.15 * cm
    x_vak = MARGE + 0.9 * cm
    vak_b = (W - MARGE - x_vak - (n - 1) * gat) / n
    vak_h, rij_h = 2.0 * cm, 2.4 * cm
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
    for g in range(pogingen):
        y = kop_y - 0.3 * cm - (g + 1) * rij_h
        c.setFont("Helvetica-Bold", 12)
        c.drawString(MARGE, y + rij_h / 2 - 0.1 * cm, str(g + 1))
        for k in range(n):
            x = x_vak + k * (vak_b + gat)
            c.setLineWidth(1)
            c.roundRect(x, y + 0.1 * cm, vak_b, vak_h, 4)
            for i, soort in enumerate(SOORTEN):
                vinkje(c, x + vak_b * (0.25 + 0.25 * i), y + 0.1 * cm + 0.4 * cm, 0.22 * cm, soort)
    p.y = kop_y - 0.3 * cm - pogingen * rij_h


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


def generate(params: dict, uit: Path) -> str:
    params = los_seed(params)
    t = TEKST.get(params["taal"], TEKST["nl"])
    taalnr = 1 if params["taal"] == "en" else 0  # kolom in CATEGORIEEN
    pr = maak_profiel(params)
    n = params["lengte"]
    naam, cats = pr["naam"], pr["cats"]

    teken_profiel(Pdf(uit / "profiel.pdf", t["profiel"].format(naam=naam)), pr, t, taalnr, params["seed"])

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"].format(naam=naam, n=n))
    for r in t["regels"]:
        p.regel("- " + r.format(n=n), 10)
    teken_schema(p, n, params["pogingen"], t)
    p.opslaan()

    letters = " ".join(LETTERS[i] for i in pr["geheim"])
    delen = " + ".join(pr["waarden"][cats[i]] for i in pr["geheim"])
    b = begeleider(uit / "begeleider.pdf", t["titel"], pr["wachtwoord"],
                   [t["oplossing"].format(naam=naam, letters=letters, delen=delen, antwoord=pr["wachtwoord"], seed=params["seed"]), t["controle"]],
                   [h.format(n=n) for h in t["hints"]], params["taal"])
    b.opslaan()
    return pr["wachtwoord"]


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
