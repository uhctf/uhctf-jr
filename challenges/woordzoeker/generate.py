"""Woordzoeker waarvan de overgebleven letters het antwoord spellen."""
import random
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, W, Pdf, begeleider

MIN_WOORDEN = 4  # een woordzoeker met minder woorden is geen puzzel
RICHTINGEN = [(0, 1), (1, 0), (1, 1), (-1, 1), (0, -1), (-1, 0), (-1, -1), (1, -1)]  # eerste vier: vooruit
TEKST = {
    "nl": {"titel": "Woordzoeker", "oplossing_titel": "oplossing", "intro": "Zoek de woorden en kruis ze af. De letters die overblijven, van links naar rechts en van boven naar onder, vormen het antwoord.",
           "oplossing": "Alle woorden staan in het raster. De {n} overgebleven letters spellen, in leesrichting, het antwoord.",
           "hints": ["Zoek eerst alle woorden uit de lijst en kruis ze af.", "Niet elke letter hoort bij een woord.",
                     "Lees de overgebleven letters in leesrichting."]},
    "en": {"titel": "Word search", "oplossing_titel": "solution", "intro": "Find the words and cross them out. The letters left over, left to right and top to bottom, are the answer.",
           "oplossing": "All words are in the grid. The {n} remaining letters spell the answer in reading order.",
           "hints": ["First find all words in the list and cross them out.", "Not every letter belongs to a word.",
                     "Read the remaining letters in reading order."]},
}


def vind(raster: list[list[str]], woord: str) -> list[list[tuple[int, int]]]:
    n = len(raster)
    gevonden = []
    for r in range(n):
        for c in range(n):
            for dr, dc in RICHTINGEN:
                cellen = [(r + i * dr, c + i * dc) for i in range(len(woord))]
                if all(0 <= x < n and 0 <= y < n and raster[x][y] == woord[i] for i, (x, y) in enumerate(cellen)):
                    gevonden.append(cellen)
    return gevonden


def maak_raster(antwoord: str, woorden: list[str], n: int, rng: random.Random, moeilijk: bool):
    antwoord = antwoord.upper()
    woorden = [w.upper() for w in woorden]
    if not antwoord.isalpha():
        raise ValueError("Het antwoord mag enkel letters bevatten")
    if not all(w.isalpha() for w in woorden):
        raise ValueError("Woorden mogen enkel letters bevatten")
    richtingen = RICHTINGEN if moeilijk else RICHTINGEN[:3]
    for _ in range(4000):
        raster = [[""] * n for _ in range(n)]
        gebruikt, plaatsen = [], {}
        pool = woorden[:]
        rng.shuffle(pool)
        pool.sort(key=len, reverse=True)
        for w in pool:
            vrij = n * n - sum(1 for r in raster for x in r if x)
            if vrij <= len(antwoord):
                break
            opties = []
            for r in range(n):
                for c in range(n):
                    for dr, dc in richtingen:
                        cellen = [(r + i * dr, c + i * dc) for i in range(len(w))]
                        if all(0 <= x < n and 0 <= y < n and raster[x][y] in ("", w[i]) for i, (x, y) in enumerate(cellen)):
                            nieuw = sum(1 for (x, y) in cellen if not raster[x][y])
                            if vrij - nieuw >= len(antwoord):
                                opties.append((cellen, nieuw))
            if not opties:
                continue
            cellen, _ = rng.choice(opties)
            for i, (x, y) in enumerate(cellen):
                raster[x][y] = w[i]
            gebruikt.append(w)
            plaatsen[w] = cellen
        vrij_cellen = [(r, c) for r in range(n) for c in range(n) if not raster[r][c]]
        if len(vrij_cellen) != len(antwoord) or len(gebruikt) < MIN_WOORDEN:
            continue
        for (r, c), letter in zip(vrij_cellen, antwoord):
            raster[r][c] = letter
        if all(len(vind(raster, w)) == 1 for w in gebruikt):
            return raster, gebruikt, plaatsen, vrij_cellen
    raise ValueError("Kon geen woordzoeker met minstens 4 woorden maken. Probeer een groter raster, een korter antwoord of meer woorden.")


def teken(p: Pdf, raster, gebruikt, markeer=None, cirkel=None) -> None:
    n = len(raster)
    cel = min((W - 2 * MARGE) / n, 2 * cm)
    x0, y0 = MARGE, p.y
    p.c.setFont("Helvetica", cel * 0.45)
    for r in range(n):
        for c in range(n):
            x, y = x0 + c * cel, y0 - (r + 1) * cel
            p.c.setLineWidth(0.6)
            p.c.rect(x, y, cel, cel)
            if markeer and (r, c) in markeer:
                p.c.setFillColorRGB(1, 0.9, 0.4)
                p.c.rect(x, y, cel, cel, fill=1)
                p.c.setFillGray(0)
            if cirkel and (r, c) in cirkel:
                p.c.setLineWidth(2)
                p.c.circle(x + cel / 2, y + cel / 2, cel * 0.42)
            p.c.setFont("Helvetica", cel * 0.45)
            p.c.drawCentredString(x + cel / 2, y + cel * 0.28, raster[r][c])
    p.c.setLineWidth(1)
    p.ruimte(n * cel + 20)
    p.regel("   ".join(sorted(gebruikt)), 11)


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, n = params["antwoord"], params["grootte"]
    rng = random.Random(params["seed"])
    raster, gebruikt, plaatsen, vrij = maak_raster(antwoord, params["woorden"], n, rng, params.get("moeilijk", False))

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    p.ruimte(8)
    teken(p, raster, gebruikt)
    p.opslaan()

    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"].format(n=len(antwoord))],
                   t["hints"], params["taal"])
    b.pagina(t["titel"] + " - " + t["oplossing_titel"])
    gemarkeerd = {cel for cellen in plaatsen.values() for cel in cellen}
    teken(b, raster, gebruikt, markeer=gemarkeerd, cirkel=set(vrij))
    b.opslaan()
    if params.get("digitaal"):
        digitaal(raster, gebruikt, uit, t)
    return antwoord


def digitaal(raster, gebruikt, uit: Path, t: dict) -> None:
    """Digitaal potlood: letters markeren en woorden doorstrepen. Onderaan staan de letters die niet gemarkeerd zijn; de pagina controleert niets."""
    css = """
.raster-cellen{display:grid;gap:4px;max-width:580px;margin:0 auto}
.cel{padding:0;aspect-ratio:1;font-family:var(--mono);font-size:clamp(16px,3.4vw,28px);font-weight:900;box-shadow:none;border-width:2px;background:#fff}
.cel:hover{background:var(--cyaan-zacht);transform:none;box-shadow:none}
.cel.gevonden{background:var(--cyaan)}
#woorden{list-style:none;padding:0;columns:3;gap:8px;margin:12px 0}
#woorden .woord{width:100%;text-align:left;box-shadow:none;border-width:2px;padding:3px 10px;margin:3px 0;font-family:var(--mono);font-size:15px;}
#woorden .woord.klaar{text-decoration:line-through;text-decoration-color:var(--magenta);text-decoration-thickness:3px;color:var(--muted);background:#ececf2}
@media(max-width:600px){#woorden{columns:2}}
"""
    body = """  <div class="kaart">
    <h2>Raster</h2>
    <div id="raster" class="raster-cellen"></div>
    <div class="rij"><button id="wis" type="button">Alle markeringen wissen</button></div>
    <p class="klein">Klik op een letter om te markeren, op een woord om door te strepen.</p>
    <ul id="woorden"></ul>
  </div>
  <div class="kaart">
    <h2>Letters die overblijven</h2>
    <div id="rest" class="antwoordbalk"></div>
  </div>"""
    gegevens = {"raster": ["".join(rij) for rij in raster], "woorden": sorted(gebruikt)}
    schrijf(uit, t["titel"], "Markeer de woorden uit de lijst. Welke letters blijven over?", body,
            Path(__file__).parent / "digitaal.js", gegevens, t["hints"], css)


def check(params: dict) -> None:
    rng = random.Random(params["seed"])
    raster, gebruikt, _, vrij = maak_raster(params["antwoord"], params["woorden"], params["grootte"], rng,
                                            params.get("moeilijk", False))
    assert all(len(vind(raster, w)) == 1 for w in gebruikt)
    assert "".join(raster[r][c] for r, c in vrij) == params["antwoord"].upper()
