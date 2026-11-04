"""Woorden verstopt onder gekleurde camouflage: door de juiste gekleurde mica verdwijnt de camouflage en zie je het woord."""
import random
import string
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont
from reportlab.lib.units import cm

from jr.pdf import MARGE, W, Pdf, begeleider
from jr.shared import gebruik

# filter -> (inkt van het woord, inkten van de camouflage, kanaal dat de filter doorlaat: 0 rood, 1 groen, 2 blauw)
# Alle camouflage-inkten zijn maximaal in het kanaal van de filter: door de filter lijken ze even licht als het papier
# en blijft enkel het woord (laag in dat kanaal) donker over. Met het blote oog breken de verschillende kleuren het woord op.
# Printers en mica's verschillen: maak altijd een testafdruk.
FILTERS = {
    "rood": ((140, 235, 255), [(255, 40, 40), (255, 140, 0), (255, 60, 170), (255, 210, 0)], 0),
    "blauw": ((255, 225, 120), [(40, 90, 255), (0, 190, 255), (170, 70, 255), (120, 160, 255)], 2),
    "groen": ((255, 140, 255), [(40, 255, 70), (0, 255, 220), (220, 255, 0), (120, 255, 120)], 1),
}
BREEDTE, HOOGTE = 1500, 520  # pixels per vak

TEKST = {
    "nl": {
        "titel": "Geheime kleuren",
        "intro": "Op dit blad staan geheime woorden, maar ze zijn verstopt onder een wirwar van kleuren.",
        "opdracht": "Kijk door de gekleurde mica's naar elk vak. Welke kleur laat welk woord zien? "
                    "Zet de woorden van vak 1, 2, ... achter elkaar.",
        "vak": "Vak {n}",
        "oplossing": "Een gekleurde filter laat enkel licht van zijn eigen kleur door. Camouflage in die kleur lijkt dan even licht "
                     "als het papier en verdwijnt; het woord in een andere kleur wordt donker.",
        "per_vak": "Vak {n}: {filter} filter -> {woord}",
        "zicht": "Zo ziet elk vak eruit door de juiste filter:",
        "filters": {"rood": "rode", "blauw": "blauwe (of cyaan)", "groen": "groene"},
        "hints": ["Kijk door elke mica naar elk vak. Wat verdwijnt er?",
                  "Een rode mica laat rode krabbels verdwijnen. Welke kleur heeft de wirwar in elk vak?",
                  "Gebruik voor elk vak de mica met dezelfde kleur als de wirwar, en zet de woorden in volgorde."],
    },
    "en": {
        "titel": "Secret colours",
        "intro": "This sheet holds secret words, but they are hidden under a jumble of colours.",
        "opdracht": "Look at each box through the coloured filters. Which colour shows which word? "
                    "Put the words of box 1, 2, ... in a row.",
        "vak": "Box {n}",
        "oplossing": "A coloured filter only lets through light of its own colour. Camouflage in that colour then looks as light "
                     "as the paper and disappears; the word in another colour turns dark.",
        "per_vak": "Box {n}: {filter} filter -> {woord}",
        "zicht": "This is what each box looks like through the right filter:",
        "filters": {"rood": "red", "blauw": "blue (or cyan)", "groen": "green"},
        "hints": ["Look at each box through each filter. What disappears?",
                  "A red filter makes red scribbles disappear. What colour is the jumble in each box?",
                  "For each box, use the filter with the same colour as the jumble, and put the words in order."],
    },
}


def delen(antwoord: str, n: int) -> list[str]:
    """Splits het antwoord in n woorden: op '-' of spatie als dat er precies n geeft, anders in gelijke stukken."""
    for sep in ("-", " "):
        stukken = [s for s in antwoord.split(sep) if s]
        if len(stukken) == n:
            return stukken
    lengte = -(-len(antwoord) // n)
    stukken = [antwoord[i * lengte:(i + 1) * lengte] for i in range(n)]
    if not all(stukken):
        raise ValueError(f"Het antwoord is te kort voor {n} vakken")
    return stukken


def lettertype(grootte: int):
    return ImageFont.load_default(size=grootte)


def maak_vak(woord: str, filter_: str, rng: random.Random) -> tuple[Image.Image, Image.Image]:
    """Geeft het vak (RGB) en het masker van het woord terug."""
    inkt, camo, _ = FILTERS[filter_]
    grootte = 300
    while lettertype(grootte).getlength(woord) > BREEDTE * 0.85:
        grootte -= 10
    dik = max(4, grootte // 25)
    masker = Image.new("L", (BREEDTE, HOOGTE), 0)
    ImageDraw.Draw(masker).text((BREEDTE / 2, HOOGTE / 2), woord, fill=255, font=lettertype(grootte),
                                anchor="mm", stroke_width=dik, stroke_fill=255)
    laag_woord = Image.new("RGB", masker.size, "white")
    laag_woord.paste(inkt, mask=masker)
    # snippers in de inkt van het woord over het hele vak, zodat die kleur niet enkel in het woord voorkomt
    d = ImageDraw.Draw(laag_woord)
    for _ in range(350):
        x, y = rng.uniform(0, BREEDTE), rng.uniform(0, HOOGTE)
        d.line([(x, y), (x + rng.uniform(-25, 25), y + rng.uniform(-25, 25))], fill=inkt, width=rng.randint(dik, 2 * dik))

    laag_camo = Image.new("RGB", masker.size, "white")
    d = ImageDraw.Draw(laag_camo)
    # nep-letters in dezelfde vorm als het woord, zodat het oog geen echt woord herkent
    for _ in range(60):
        g, kleur = int(grootte * rng.uniform(0.3, 0.8)), rng.choice(camo)
        d.text((rng.uniform(0, BREEDTE), rng.uniform(0, HOOGTE)), rng.choice(string.ascii_uppercase), fill=kleur,
               font=lettertype(g), anchor="mm", stroke_width=max(2, g // 25), stroke_fill=kleur)
    # fijne krabbels, ongeveer zo dik als de letters van het woord, zodat de randen van het woord wegvallen
    for _ in range(900):
        x, y, lengte = rng.uniform(0, BREEDTE), rng.uniform(0, HOOGTE), rng.uniform(20, 90)
        punten = [(x, y), (x + rng.uniform(-lengte, lengte), y + rng.uniform(-lengte, lengte)),
                  (x + rng.uniform(-lengte, lengte), y + rng.uniform(-lengte, lengte))]
        d.line(punten, fill=rng.choice(camo), width=rng.randint(dik, 4 * dik), joint="curve")
    # Inkt op inkt: vermenigvuldigen, zoals bij drukken. Zo blijft het woord donker door de filter, ook onder de camouflage.
    return ImageChops.multiply(laag_woord, laag_camo), masker


def door_filter(vak: Image.Image, filter_: str) -> Image.Image:
    """Wat je ziet door de filter: enkel het kanaal van die kleur, in grijstinten."""
    return vak.getchannel(FILTERS[filter_][2])


def maak(params: dict):
    filters = params["filters"]
    onbekend = [f for f in filters if f not in FILTERS]
    if onbekend or not filters:
        raise ValueError(f"Onbekende filters {onbekend}. Mogelijk: {', '.join(FILTERS)}")
    woorden = [w.upper() for w in delen(params["antwoord"], len(filters))]
    rng = random.Random(params["seed"])
    return woorden, [maak_vak(w, f, rng) for w, f in zip(woorden, filters)]


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, filters = params["antwoord"], params["filters"]
    woorden, vakken = maak(params)

    # alle vakken onder elkaar in één afbeelding, voor de beeldbewerker of om groot te printen
    marge = 40
    blad = Image.new("RGB", (BREEDTE, len(vakken) * (HOOGTE + marge) - marge), "white")
    for i, (vak, _) in enumerate(vakken):
        blad.paste(vak, (0, i * (HOOGTE + marge)))
    blad.save(uit / "kleuren.png")

    breedte = W - 2 * MARGE
    hoogte = breedte * HOOGTE / BREEDTE
    with tempfile.TemporaryDirectory() as tmp:
        p = Pdf(uit / "deelnemer.pdf", t["titel"])
        p.regel(t["intro"])
        p.regel(t["opdracht"])
        for i, (vak, _) in enumerate(vakken, 1):
            pad = Path(tmp) / f"vak{i}.png"
            vak.save(pad)
            if p.y - hoogte < MARGE + 2 * cm:
                p.pagina(t["titel"])
            p.kop(t["vak"].format(n=i))
            p.ruimte(hoogte)
            p.c.drawImage(str(pad), MARGE, p.y, breedte, hoogte)
            p.c.rect(MARGE, p.y, breedte, hoogte)
            p.ruimte(12)
        p.opslaan()

        per_vak = [t["per_vak"].format(n=i, filter=t["filters"][f], woord=w) for i, (f, w) in enumerate(zip(filters, woorden), 1)]
        b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"]] + per_vak, t["hints"], params["taal"])
        b.kop(t["zicht"])
        klein = breedte * 0.6
        for i, ((vak, _), f) in enumerate(zip(vakken, filters), 1):
            pad = Path(tmp) / f"zicht{i}.png"
            door_filter(vak, f).save(pad)
            if b.y - klein * HOOGTE / BREEDTE < MARGE + 2 * cm:
                b.pagina(t["titel"])
            b.ruimte(klein * HOOGTE / BREEDTE)
            b.c.drawImage(str(pad), MARGE, b.y, klein, klein * HOOGTE / BREEDTE)
            b.ruimte(10)
        b.opslaan()

    if params["met_beeldbewerker"]:
        gebruik(uit, params["taal"], "beeldbewerker", opties={"beeldbewerker": {"afbeelding": str(uit / "kleuren.png")}})
    return antwoord


def check(params: dict) -> None:
    """Door de juiste filter moet het woord duidelijk donkerder zijn dan de camouflage."""
    _, vakken = maak(params)
    for (vak, masker), f in zip(vakken, params["filters"]):
        zicht = door_filter(vak, f)
        woord = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m > 128]
        rest = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m == 0]
        verschil = sum(rest) / len(rest) - sum(woord) / len(woord)
        assert verschil > 90, f"te weinig contrast door de {f} filter ({verschil:.0f})"
