"""Kies je kant: kaartjes met een grijs gearceerde achtergrond en een kleurcode. Wie dezelfde kleur afleest uit de code, hoort bij dezelfde ploeg."""
import random
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.units import cm

from jr.pdf import MARGE, W, Pdf, begeleider

TEKST = {
    "titel": "Kies je kant",
    "intro": "Knip de kaartjes uit en deel ze om en om uit.",
    "uitleg": ["Uitleg voor op het bord (niet op de kaartjes):",
               "Een kleurcode bestaat uit drie paren: rood, groen, blauw. Elk paar loopt van 00 (uit) tot FF (aan)."],
    "oplossing": ["Op elk kaartje staat een kleurcode op een grijze, gearceerde achtergrond: de achtergrond zegt niets over de kleur. Cyaan is blauwgroen, Magenta is roze-paars.",
                  "Een kleurcode bestaat uit drie paren hexadecimale cijfers: rood, groen en blauw. Een paar dat met 0 tot 7 begint, is laag; met 8 tot F is het hoog. Op elk kaartje is precies één paar laag: rood laag is Cyaan, groen laag is Magenta.",
                  "Deel de kaartjes in de volgorde van de stapel uit: er komt telkens één Cyaan en één Magenta. Hieronder staat bij elk kaartje de juiste kleur.",
                  "De deelnemers zoeken elkaar: wie dezelfde kleur heeft, hoort bij dezelfde ploeg. Ze mogen elkaars kaartjes bekijken, maar de kleur niet hardop zeggen. Controleer daarna of de ploegen even groot zijn.",
                  "Cyaan en Magenta strijden tegen elkaar. Op het scoreblad hieronder noteren jullie per team hoeveel sloten open zijn en wanneer de kluis opengaat."],
    "hints": ["De grijze achtergrond zegt niets. Kijk naar de code.",
              "De code bestaat uit drie paren (rood, groen, blauw). Een paar dat met 0 tot 7 begint, is laag; één paar is laag.",
              "Rood laag is Cyaan, groen laag is Magenta."],
    "kolommen": ("Kaartje", "Code", "Kleur"),
    "score_kop": "Scoreblad",
    "score_kolommen": ("Helft", "Team", "Sloten open", "Kluis open om"),
}

HOOG = (0xC0, 0x100)  # twee waarden hoog, zodat de kleur duidelijk Cyaan of Magenta is
LAAG = (0x00, 0x40)


def maak_kaartjes(params: dict) -> list[tuple[str, str]]:
    """Lijst van (code, kleur), per twee één Cyaan en één Magenta in willekeurige volgorde."""
    aantal = params["aantal"]
    if aantal < 2 or aantal % 2:
        raise ValueError("aantal moet even zijn en minstens 2")
    rng = random.Random(params["seed"])
    hoog, laag = lambda: rng.randrange(*HOOG), lambda: rng.randrange(*LAAG)  # noqa: E731
    kaartjes, gezien = [], set()
    while len(kaartjes) < aantal:
        paar = []
        for kleur in ("Cyaan", "Magenta"):
            while True:
                r, g, b = (laag(), hoog(), hoog()) if kleur == "Cyaan" else (hoog(), laag(), hoog())
                code = f"#{r:02X}{g:02X}{b:02X}"
                if code not in gezien:
                    gezien.add(code)
                    break
            paar.append((code, kleur))
        rng.shuffle(paar)
        kaartjes += paar
    return kaartjes


def kleur_van(code: str) -> str:
    r, g = int(code[1:3], 16), int(code[3:5], 16)
    return "Cyaan" if r < g else "Magenta"


def teken_kaartje(c, x: float, y: float, breedte: float, hoogte: float, code: str, grijs: float) -> None:
    """Gearceerde achtergrond in grijs (zegt niets over de kleur), met de code in een wit vak."""
    rgb = [grijs] * 3
    c.saveState()
    pad = c.beginPath()
    pad.rect(x, y, breedte, hoogte)
    c.clipPath(pad, stroke=0, fill=0)
    c.setFillColor(Color(*[0.3 * v + 0.7 for v in rgb]))  # lichte tint van het grijs
    c.rect(x, y, breedte, hoogte, stroke=0, fill=1)
    c.setStrokeColor(Color(*rgb))
    c.setLineWidth(4)
    stap = 0.45 * cm
    k = -hoogte
    while k < breedte:  # schuine strepen
        c.line(x + k, y, x + k + hoogte, y + hoogte)
        k += stap
    c.restoreState()
    vak_b, vak_h = 5.6 * cm, 1.4 * cm
    vx, vy = x + (breedte - vak_b) / 2, y + (hoogte - vak_h) / 2
    c.setFillColorRGB(1, 1, 1)
    c.setStrokeColorRGB(0.13, 0.13, 0.13)
    c.setLineWidth(2)
    c.rect(vx, vy, vak_b, vak_h, stroke=1, fill=1)
    c.setFillColorRGB(0.13, 0.13, 0.13)
    c.setFont("Courier-Bold", 26)
    c.drawCentredString(x + breedte / 2, vy + 0.42 * cm, code)
    c.setStrokeColorRGB(0, 0, 0)
    c.setDash(3, 3)
    c.setLineWidth(0.6)
    c.rect(x, y, breedte, hoogte)
    c.setDash()


def generate(params: dict, uit: Path) -> None:
    t = TEKST
    kaartjes = maak_kaartjes(params)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    for i, regel in enumerate(t["uitleg"]):
        p.regel(regel, 10 if i else 11)
    p.ruimte(6)
    rng = random.Random(f"{params['seed']}-grijs")  # los van de codes: elk kaartje een ander grijs
    kolommen, rijen = 2, 5  # 10 per pagina
    breedte, hoogte = (W - 2 * MARGE) / kolommen, 3.9 * cm
    per_pagina = kolommen * rijen
    for i, (code, _) in enumerate(kaartjes):
        if i and i % per_pagina == 0:
            p.pagina(t["titel"])
        k, r = i % per_pagina % kolommen, i % per_pagina // kolommen
        teken_kaartje(p.c, MARGE + k * breedte, p.y - (r + 1) * hoogte, breedte, hoogte, code, rng.uniform(0.25, 0.65))
    p.opslaan()

    g = begeleider(uit / "begeleider.pdf", t["titel"], None, t["oplossing"], t["hints"], params["taal"])
    g.tabel(t["kolommen"], [(str(i), code, kleur) for i, (code, kleur) in enumerate(kaartjes, 1)], (3 * cm, 5 * cm, 5 * cm), 11)
    g.pagina(t["titel"] + " - " + t["score_kop"])
    g.kop(t["score_kop"])
    rijen = [(helft, "", "", "") for helft in ("Cyaan", "Magenta") for _ in range(5)]
    g.tabel(t["score_kolommen"], rijen, (3 * cm, 6 * cm, 3.5 * cm, 4 * cm), 12)
    g.opslaan()
    return None


def check(params: dict) -> None:
    kaartjes = maak_kaartjes(params)
    assert len(kaartjes) == params["aantal"]
    assert len({code for code, _ in kaartjes}) == len(kaartjes), "kleurcodes moeten verschillen"
    assert sum(k == "Cyaan" for _, k in kaartjes) == len(kaartjes) // 2, "helften moeten even groot zijn"
    for code, kleur in kaartjes:
        waarden = [int(code[i:i + 2], 16) for i in (1, 3, 5)]
        assert sum(w < 0x80 for w in waarden) == 1, f"{code}: precies één lage waarde"
        assert kleur_van(code) == kleur
