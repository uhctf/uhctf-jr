"""Kartonnen kaarten met gaten (Cardan-rooster): leg elke kaart op de juiste bladzijde en lees een woord door de gaten."""
import random
import re
from pathlib import Path

from reportlab.lib.units import cm

from jr.pdf import H, MARGE, W, Pdf, begeleider

# Kader van het rooster: zelfde plek op de bladzijden en op de kaarten, zodat ze precies op elkaar passen.
KADER_X, KADER_B = MARGE, W - 2 * MARGE
KADER_TOP, KADER_H = H - MARGE - 1.6 * cm, 22 * cm
RAND, RAND_TOP = 0.3 * cm, 0.8 * cm  # rand rond het rooster; bovenaan is plaats voor het kaartnummer

ZINNEN = {
    "nl": [
        "de bibliothecaris sloot elke avond om negen uur de zware deur",
        "niemand wist waarom het oude boek altijd op dezelfde plank lag",
        "achter de kast hoorde je soms het zachte tikken van een klok",
        "de sleutel hing aan een rode draad naast het raam",
        "op zolder stonden dozen vol brieven die nooit verstuurd waren",
        "het meisje las elke bladzijde twee keer om niets te missen",
        "een kat sliep op de vensterbank in de warme zon",
        "de kaart van de stad was gescheurd in vier stukken",
        "wie goed kijkt ziet dat sommige letters anders zijn",
        "de regen tikte de hele nacht tegen de ramen van het huis",
        "in de kelder stond een kist met een slot van koper",
        "de oude man schreef zijn geheimen in een klein notitieboek",
        "elke dinsdag kwam de postbode met een pakje zonder naam",
        "de trap kraakte bij elke stap die iemand zette",
        "boven de deur hing een bord met een vreemde tekening",
        "de lamp flikkerde even en toen werd het helemaal donker",
        "in de tuin groeiden bloemen in alle kleuren van de regenboog",
        "de wind blies de bladeren van de bomen over het plein",
        "het was stil in de leeszaal op het zachte ritselen na",
        "op het bureau lag een vergrootglas naast een stapel papier",
        "de vos sprong over de lage muur en verdween in het bos",
        "iemand had met potlood kleine kruisjes in de kantlijn gezet",
        "de bakker gaf de kinderen elke ochtend een warm broodje",
        "de trein vertrok precies op tijd naar de kust",
    ],
    "en": [
        "the librarian closed the heavy door every evening at nine",
        "nobody knew why the old book was always on the same shelf",
        "behind the cupboard you could sometimes hear a clock ticking",
        "the key hung from a red thread next to the window",
        "in the attic there were boxes full of letters never sent",
        "the girl read every page twice so she would miss nothing",
        "a cat slept on the windowsill in the warm sun",
        "the map of the city was torn into four pieces",
        "if you look closely you see that some letters are different",
        "the rain tapped against the windows of the house all night",
        "in the cellar stood a chest with a copper lock",
        "the old man wrote his secrets in a small notebook",
        "every tuesday the postman came with a parcel without a name",
        "the stairs creaked with every step anyone took",
        "above the door hung a sign with a strange drawing",
        "the lamp flickered for a moment and then it went dark",
        "in the garden grew flowers in all the colours of the rainbow",
        "the wind blew the leaves from the trees across the square",
        "it was quiet in the reading room apart from soft rustling",
        "on the desk lay a magnifying glass next to a pile of paper",
        "the fox jumped over the low wall and vanished into the woods",
        "someone had drawn small crosses in the margin with a pencil",
        "the baker gave the children a warm roll every morning",
        "the train left for the coast exactly on time",
    ],
}

TEKST = {
    "nl": {
        "titel": "Gatenkaart",
        "intro": "Dit boek lijkt saai, maar er zit een geheime zin in verstopt. Je krijgt een paar kartonnen kaarten met gaten. "
                 "Elke kaart past op precies één bladzijde.",
        "opdracht": "Leg een kaart op een bladzijde: de rand van de kaart valt precies op het kader, met 'boven' bovenaan. "
                    "Lees de letters door de gaten, van links naar rechts en van boven naar onder. "
                    "Vind je een echt woord? Dan heb je de juiste bladzijde. Zet de woorden van kaart 1, 2, 3, ... achter elkaar.",
        "boek": "Het geheime boek",
        "kaart": "Kaart {n}",
        "boven": "boven",
        "knippen": "Plak op karton, snij langs de buitenrand en snij de grijze vakjes uit.",
        "oplossing": "Elke kaart past op één bladzijde. Leg de kaart op het kader en lees de letters door de gaten, in leesvolgorde.",
        "per_kaart": "Kaart {n} op blz. {blz}: {woord}",
        "hints": ["Probeer een kaart op elke bladzijde. Op de meeste bladzijden zie je onzin.",
                  "Lees de gaten zoals je een boek leest: rij per rij, van links naar rechts.",
                  "Elke kaart geeft één woord. Zet ze in de volgorde van de kaartnummers."],
    },
    "en": {
        "titel": "Hole card",
        "intro": "This book looks boring, but a secret sentence is hidden in it. You get a few cardboard cards with holes. "
                 "Each card fits on exactly one page.",
        "opdracht": "Put a card on a page: the edge of the card lines up with the frame, with 'top' at the top. "
                    "Read the letters through the holes, left to right and top to bottom. "
                    "Do you find a real word? Then you have the right page. Put the words of card 1, 2, 3, ... in a row.",
        "boek": "The secret book",
        "kaart": "Card {n}",
        "boven": "top",
        "knippen": "Glue onto cardboard, cut along the outer edge and cut out the grey boxes.",
        "oplossing": "Each card fits on one page. Put the card on the frame and read the letters through the holes, in reading order.",
        "per_kaart": "Card {n} on p. {blz}: {woord}",
        "hints": ["Try a card on every page. On most pages you will see nonsense.",
                  "Read the holes like you read a book: row by row, left to right.",
                  "Each card gives one word. Put them in the order of the card numbers."],
    },
}


def woorden(antwoord: str) -> list[str]:
    ws = antwoord.lower().split()
    if not ws or not all(re.fullmatch(r"[a-z]+", w) for w in ws):
        raise ValueError("Het antwoord moet uit woorden met enkel letters (a-z) bestaan, gescheiden door spaties")
    return ws


def vul_pagina(zinnen: list[str], kol: int, rij: int, rng: random.Random) -> list[str]:
    """Rij voor rij tekst, zonder woorden af te breken. Elke rij is precies 'kol' tekens breed."""
    regels, huidig, volgorde = [], "", []
    while len(regels) < rij:
        if not volgorde:  # geen zin twee keer, tot ze allemaal gebruikt zijn
            volgorde = rng.sample(zinnen, len(zinnen))
        for woord in (volgorde.pop() + ".").split():
            if len(huidig) + len(woord) + 1 > kol:
                regels.append(huidig.ljust(kol))
                huidig = ""
            huidig = f"{huidig} {woord}" if huidig else woord
    return regels[:rij]


def kies_gaten(pagina: list[str], woord: str, rng: random.Random) -> list[tuple[int, int]]:
    """Kies per letter een cel die die letter al bevat, verspreid over de bladzijde en in leesvolgorde.
    Lukt dat niet in een stuk, dan wordt een letter overschreven (zeldzaam, bv. bij q of x)."""
    kol = len(pagina[0])
    cellen = [(r, k) for r in range(len(pagina)) for k in range(kol)]
    stuk = len(cellen) // len(woord)
    gaten = []
    for i, letter in enumerate(woord):
        deel = cellen[i * stuk:(i + 1) * stuk]
        # niet op de rand van een stuk, zodat twee gaten nooit naast elkaar liggen
        deel = deel[1:-1]
        passend = [c for c in deel if pagina[c[0]][c[1]] == letter]
        if passend:
            gaten.append(rng.choice(passend))
            continue
        r, k = rng.choice([c for c in deel if pagina[c[0]][c[1]].isalpha()] or deel)
        pagina[r] = pagina[r][:k] + letter + pagina[r][k + 1:]
        gaten.append((r, k))
    return gaten


def lees(pagina: list[str], gaten: list[tuple[int, int]]) -> str:
    return "".join(pagina[r][k] for r, k in sorted(gaten))


def maak(params: dict):
    ws = woorden(params["antwoord"])
    kol, rij, n = params["kolommen"], params["rijen"], params["paginas"]
    if len(ws) > n:
        raise ValueError(f"{len(ws)} woorden maar maar {n} bladzijden: verhoog 'paginas'")
    if max(len(w) for w in ws) * 3 > kol * rij:
        raise ValueError("Een woord is te lang voor het rooster: verhoog 'kolommen' of 'rijen'")
    rng = random.Random(params["seed"])
    zinnen = ZINNEN.get(params["taal"], ZINNEN["nl"])
    for _ in range(100):
        paginas = [vul_pagina(zinnen, kol, rij, rng) for _ in range(n)]
        doelen = rng.sample(range(n), len(ws))
        kaarten = [kies_gaten(paginas[d], w, rng) for d, w in zip(doelen, ws)]
        # een kaart mag op geen enkele andere bladzijde een woord van de zin geven
        if all(lees(p, g) not in ws for g, d in zip(kaarten, doelen) for i, p in enumerate(paginas) if i != d):
            break
    else:
        raise ValueError("Geen geldige puzzel gevonden; probeer een andere seed")
    eerste = rng.randint(11, 180)
    nummers = list(range(eerste, eerste + n))
    return ws, paginas, kaarten, doelen, nummers


def rooster(kol: int, rij: int):
    """Linkerbovenhoek en celgrootte van het rooster binnen het kader."""
    x0, y0 = KADER_X + RAND, KADER_TOP - RAND_TOP
    return x0, y0, (KADER_B - 2 * RAND) / kol, (KADER_H - RAND_TOP - RAND) / rij


def teken_pagina(p: Pdf, pagina: list[str], nummer: int, gemarkeerd=()) -> None:
    c = p.c
    kol, rij = len(pagina[0]), len(pagina)
    x0, y0, cw, ch = rooster(kol, rij)
    c.setLineWidth(1)
    c.rect(KADER_X, KADER_TOP - KADER_H, KADER_B, KADER_H)
    if gemarkeerd:
        c.setFillColorRGB(1, 0.75, 0.9)
        for r, k in gemarkeerd:
            c.rect(x0 + k * cw, y0 - (r + 1) * ch, cw, ch, stroke=0, fill=1)
        c.setFillGray(0)
    grootte = min(cw / 0.6 * 0.8, ch * 0.7)
    c.setFont("Courier", grootte)
    for r, regel in enumerate(pagina):
        for k, letter in enumerate(regel):
            if letter != " ":
                c.drawCentredString(x0 + (k + 0.5) * cw, y0 - (r + 1) * ch + ch * 0.3, letter)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W / 2, KADER_TOP - KADER_H - 0.7 * cm, f"- {nummer} -")


def teken_kaart(p: Pdf, gaten, kol: int, rij: int, t: dict, n: int) -> None:
    c = p.c
    x0, y0, cw, ch = rooster(kol, rij)
    c.setLineWidth(1.5)
    c.setDash(6, 3)
    c.rect(KADER_X, KADER_TOP - KADER_H, KADER_B, KADER_H)
    c.setDash()
    c.setFont("Helvetica-Bold", 12)
    c.drawString(KADER_X + RAND, KADER_TOP - 0.55 * cm, t["kaart"].format(n=n))
    c.drawRightString(KADER_X + KADER_B - RAND, KADER_TOP - 0.55 * cm, t["boven"].upper())
    c.setLineWidth(0.8)
    c.setFillGray(0.75)
    for r, k in gaten:
        # iets kleiner dan de cel, zodat je enkel die ene letter ziet
        c.rect(x0 + k * cw + cw * 0.1, y0 - (r + 1) * ch + ch * 0.1, cw * 0.8, ch * 0.8, fill=1)
    c.setFillGray(0)
    c.setFont("Helvetica", 9)
    c.drawString(KADER_X, KADER_TOP - KADER_H - 0.6 * cm, t["knippen"])


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    ws, paginas, kaarten, doelen, nummers = maak(params)
    kol, rij = params["kolommen"], params["rijen"]
    antwoord = " ".join(ws)

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    p.regel(t["opdracht"])
    for pagina, nummer in zip(paginas, nummers):
        p.pagina(t["boek"])
        teken_pagina(p, pagina, nummer)
    p.opslaan()

    k = Pdf(uit / "kaarten.pdf", t["kaart"].format(n=1))
    for i, gaten in enumerate(kaarten, 1):
        if i > 1:
            k.pagina(t["kaart"].format(n=i))
        teken_kaart(k, gaten, kol, rij, t, i)
    k.opslaan()

    per_kaart = [t["per_kaart"].format(n=i, blz=nummers[d], woord=w) for i, (d, w) in enumerate(zip(doelen, ws), 1)]
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"]] + per_kaart, t["hints"], params["taal"])
    for i, (gaten, d) in enumerate(zip(kaarten, doelen), 1):
        b.pagina(t["kaart"].format(n=i) + f" - {nummers[d]}")
        teken_pagina(b, paginas[d], nummers[d], gaten)
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    ws, paginas, kaarten, doelen, _ = maak(params)
    for w, gaten, d in zip(ws, kaarten, doelen):
        assert lees(paginas[d], gaten) == w, f"kaart voor '{w}' leest '{lees(paginas[d], gaten)}'"
        assert len(set(gaten)) == len(gaten)
        for i, p in enumerate(paginas):
            assert i == d or lees(p, gaten) not in ws
