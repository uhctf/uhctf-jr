"""Doolhof met een woord langs de juiste route, en afleidende letters ernaast."""
import random
import string
from collections import deque
from pathlib import Path

from reportlab.lib.units import cm

from jr.pdf import H, MARGE, W, Pdf, begeleider

TEKST = {
    "nl": {"titel": "Doolhof", "intro": "Vind je weg door het doolhof van Start naar Einde. De reis brengt de beloning: "
                                         "schrijf de letters op die je onderweg tegenkomt.",
           "start": "Start", "einde": "Einde", "oplossing_titel": "oplossing",
           "oplossing": "Volg de route van Start naar Einde en lees de letters in volgorde. Letters naast de route zijn afleiding.",
           "hints": ["Het doolhof staat vol letters.", "Volg de route van Start naar Einde.",
                     "Schrijf enkel de letters op die op jouw route staan, in de juiste volgorde."]},
    "en": {"titel": "Maze", "intro": "Find your way through the maze from Start to End. The journey brings the reward: "
                                     "write down the letters you meet along the way.",
           "start": "Start", "einde": "End", "oplossing_titel": "solution",
           "oplossing": "Follow the route from Start to End and read the letters in order. Letters off the route are decoys.",
           "hints": ["The maze is full of letters.", "Follow the route from Start to End.",
                     "Only write down the letters on your route, in the right order."]},
}
BUREN = {"N": (0, -1), "S": (0, 1), "W": (-1, 0), "O": (1, 0)}
TEGEN = {"N": "S", "S": "N", "W": "O", "O": "W"}


def maak_doolhof(b: int, h: int, rng: random.Random) -> dict:
    """Perfect doolhof (depth-first). Geeft voor elke cel de set open richtingen."""
    open_ = {(x, y): set() for x in range(b) for y in range(h)}
    gezien, stapel = {(0, 0)}, [(0, 0)]
    while stapel:
        x, y = stapel[-1]
        opties = [(d, (x + dx, y + dy)) for d, (dx, dy) in BUREN.items()
                  if (x + dx, y + dy) in open_ and (x + dx, y + dy) not in gezien]
        if not opties:
            stapel.pop()
            continue
        d, nxt = rng.choice(opties)
        open_[(x, y)].add(d)
        open_[nxt].add(TEGEN[d])
        gezien.add(nxt)
        stapel.append(nxt)
    return open_


def route(open_: dict, start, einde) -> list:
    vorige, wachtrij = {start: None}, deque([start])
    while wachtrij:
        cel = wachtrij.popleft()
        if cel == einde:
            break
        for d in open_[cel]:
            nxt = (cel[0] + BUREN[d][0], cel[1] + BUREN[d][1])
            if nxt not in vorige:
                vorige[nxt] = cel
                wachtrij.append(nxt)
    pad, cel = [], einde
    while cel is not None:
        pad.append(cel)
        cel = vorige[cel]
    return pad[::-1]


def maak(params: dict):
    antwoord = params["antwoord"].upper()
    if not antwoord.isalnum():
        raise ValueError("Het antwoord mag enkel letters en cijfers bevatten")
    b, h = params["breedte"], params["hoogte"]
    rng = random.Random(params["seed"])
    for _ in range(200):
        open_ = maak_doolhof(b, h, rng)
        start, einde = (rng.randrange(b), 0), (rng.randrange(b), h - 1)
        pad = route(open_, start, einde)
        if len(pad) >= 2 * len(antwoord):
            break
    else:
        raise ValueError("Het doolhof is te klein voor dit antwoord. Verhoog breedte of hoogte.")
    # Verdeel de letters gelijkmatig over de route.
    n = len(antwoord)
    plek = [round(i * (len(pad) - 2) / (n - 1)) + 1 if n > 1 else 1 for i in range(n)]
    letters = {pad[p]: antwoord[i] for i, p in enumerate(plek)}
    afleiding = {}
    for cel in open_:
        if cel not in pad and rng.random() < 0.35:
            afleiding[cel] = rng.choice(string.ascii_uppercase)
    return open_, start, einde, pad, letters, afleiding


def lees_route(pad: list, letters: dict, afleiding: dict) -> str:
    assert not any(c in afleiding for c in pad), "afleiding op de route"
    return "".join(letters.get(c, "") for c in pad)


def teken(p: Pdf, params, data, t, toon_route=False) -> None:
    open_, start, einde, pad, letters, afleiding = data
    b, h = params["breedte"], params["hoogte"]
    cel = min((W - 2 * MARGE) / b, (p.y - MARGE - 2 * cm) / h)
    x0 = (W - cel * b) / 2
    top = p.y - 1 * cm
    c = p.c

    def pos(cx, cy):
        return x0 + cx * cel, top - cy * cel

    if toon_route:
        c.setStrokeColorRGB(0.85, 0.15, 0.25)
        c.setLineWidth(3)
        pts = [(pos(x, y)[0] + cel / 2, pos(x, y)[1] - cel / 2) for x, y in pad]
        for (ax, ay), (bx, by) in zip(pts, pts[1:]):
            c.line(ax, ay, bx, by)
        c.setStrokeGray(0)
    c.setLineWidth(1.8)
    for (cx, cy), richtingen in open_.items():
        x, y = pos(cx, cy)
        if "N" not in richtingen and not ((cx, cy) == start):
            c.line(x, y, x + cel, y)
        if "S" not in richtingen and not ((cx, cy) == einde):
            c.line(x, y - cel, x + cel, y - cel)
        if "W" not in richtingen:
            c.line(x, y, x, y - cel)
        if "O" not in richtingen:
            c.line(x + cel, y, x + cel, y - cel)
    c.setLineWidth(1)
    c.setFont("Helvetica-Bold", cel * 0.5)
    for (cx, cy), letter in {**afleiding, **letters}.items():
        x, y = pos(cx, cy)
        c.drawCentredString(x + cel / 2, y - cel * 0.68, letter)
    c.setFont("Helvetica", 12)
    sx, sy = pos(*start)
    ex, ey = pos(*einde)
    c.drawCentredString(sx + cel / 2, sy + 8, t["start"])
    c.drawCentredString(ex + cel / 2, ey - cel - 16, t["einde"])


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    data = maak(params)
    antwoord = params["antwoord"]

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    teken(p, params, data, t)
    p.opslaan()

    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"]], t["hints"], params["taal"])
    b.pagina(t["titel"] + " - " + t["oplossing_titel"])
    teken(b, params, data, t, toon_route=True)
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    open_, start, einde, pad, letters, afleiding = maak(params)
    assert lees_route(pad, letters, afleiding) == params["antwoord"].upper()
