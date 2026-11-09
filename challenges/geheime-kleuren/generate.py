"""Woorden over elkaar in een afbeelding, elk in een andere inkt: door elke gekleurde mica zie je één woord.
De volgorde van de kleuren (de kleurcode) maakt van de woorden een zin. Zijn er meer woorden dan kleuren,
dan komen er meer vakken bij en geldt de kleurcode per vak."""
import random
import tempfile
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont
from reportlab.lib.units import cm

from jr.pdf import MARGE, W, Pdf, begeleider
from jr.shared import gebruik

# filter -> (inkt van het woord, kanaal dat de filter doorlaat: 0 rood, 1 groen, 2 blauw, kleur op de kleurcode)
# Elke inkt is donker in precies één kanaal en licht in de andere twee (cyaan, magenta, geel, zoals printerinkt).
# Door een filter zie je dus enkel het woord in de inkt die dat licht tegenhoudt; de andere woorden lijken papier.
# Meer dan drie kan niet in één vak: een gele, magenta of cyaan filter laat twee kanalen door en toont twee woorden door elkaar.
# Printers en mica's verschillen: maak altijd een testafdruk.
FILTERS = {
    "rood": ((40, 255, 255), 0, (0.9, 0.1, 0.1)),
    "groen": ((255, 40, 255), 1, (0.1, 0.65, 0.2)),
    "blauw": ((255, 255, 40), 2, (0.1, 0.3, 0.9)),
}
BREEDTE, HOOGTE = 1500, 750  # pixels per vak

TEKST = {
    "nl": {
        "titel": "Geheime kleuren",
        "intro": "In deze wirwar van kleuren zit een geheime zin verstopt.",
        "opdracht": "Kijk door de gekleurde mica's naar de afbeelding. Elke kleur toont een ander woord. "
                    "Volg de kleurcode om de woorden in de juiste volgorde te zetten.",
        "opdracht_vakken": "Kijk door de gekleurde mica's naar de vakken. Elke kleur toont een ander woord. "
                           "Volg de kleurcode in vak 1, dan in vak 2, ... om de woorden in de juiste volgorde te zetten.",
        "vak": "Vak {n}",
        "kleurcode": "Kleurcode",
        "kleurcode_uitleg": "Kijk in deze volgorde door de mica's.",
        "kleurcode_vakken": "Kijk in deze volgorde door de mica's, eerst in vak 1, dan in vak 2, ...",
        "oplossing": "Elk woord is gedrukt in een inkt die precies één kleur licht tegenhoudt. Door een filter van die kleur wordt "
                     "dat woord donker; de andere woorden laten het licht door en lijken even licht als het papier. "
                     "Volg de kleurcode en lees de woorden na elkaar.",
        "per_filter": "{n}. {vak}, {filter} filter -> {woord}",
        "zicht": "Zo ziet elk vak eruit door elke filter, in de volgorde van de kleurcode:",
        "filters": {"rood": "rode", "groen": "groene", "blauw": "blauwe"},
        "hints": ["Kijk door elke mica. Zie je telkens iets anders?",
                  "Elke kleur mica toont één woord. Schrijf op welk woord bij welke kleur hoort.",
                  "Zet de woorden in de volgorde van de kleurcode."],
    },
    "en": {
        "titel": "Secret colours",
        "intro": "A secret sentence is hidden in this jumble of colours.",
        "opdracht": "Look at the image through the coloured filters. Each colour shows a different word. "
                    "Follow the colour code to put the words in the right order.",
        "opdracht_vakken": "Look at the boxes through the coloured filters. Each colour shows a different word. "
                           "Follow the colour code in box 1, then in box 2, ... to put the words in the right order.",
        "vak": "Box {n}",
        "kleurcode": "Colour code",
        "kleurcode_uitleg": "Look through the filters in this order.",
        "kleurcode_vakken": "Look through the filters in this order, first in box 1, then in box 2, ...",
        "oplossing": "Each word is printed in an ink that blocks exactly one colour of light. Through a filter of that colour the word "
                     "turns dark; the other words let the light through and look as light as the paper. "
                     "Follow the colour code and read the words one after the other.",
        "per_filter": "{n}. {vak}, {filter} filter -> {woord}",
        "zicht": "This is what each box looks like through each filter, in the order of the colour code:",
        "filters": {"rood": "red", "groen": "green", "blauw": "blue"},
        "hints": ["Look through each filter. Do you see something different each time?",
                  "Each filter colour shows one word. Write down which word goes with which colour.",
                  "Put the words in the order of the colour code."],
    },
}


def lettertype(grootte: int):
    return ImageFont.load_default(size=grootte)


def woordmasker(woord: str, rng: random.Random) -> Image.Image:
    """Het woord, groot, een beetje verschoven en gedraaid, zodat de woorden niet netjes op elkaar liggen."""
    grootte = 450
    while lettertype(grootte).getlength(woord) > BREEDTE * 0.85:
        grootte -= 10
    masker = Image.new("L", (BREEDTE, HOOGTE), 0)
    midden = (BREEDTE / 2 + rng.uniform(-80, 80), HOOGTE / 2 + rng.uniform(-HOOGTE / 10, HOOGTE / 10))
    ImageDraw.Draw(masker).text(midden, woord, fill=255, font=lettertype(grootte), anchor="mm",
                                stroke_width=max(4, grootte // 25), stroke_fill=255)
    return masker.rotate(rng.uniform(-10, 10), resample=Image.BICUBIC, center=midden)


def maak_vak(woorden: list[str], volgorde: list[str], snippers: int, rng: random.Random):
    """Eén vak met de woorden over elkaar, het eerste woord in de inkt van de eerste kleur, enzovoort.
    Geeft de afbeelding en per woord het masker terug.
    Heeft het vak minder woorden dan kleuren, dan krijgen de overige kleuren enkel snippers: zo blijft de wirwar even dicht."""
    beeld = Image.new("RGB", (BREEDTE, HOOGTE), "white")
    maskers = []
    for i, f in enumerate(volgorde):
        inkt = FILTERS[f][0]
        masker = woordmasker(woorden[i], rng) if i < len(woorden) else Image.new("L", (BREEDTE, HOOGTE), 0)
        laag = Image.new("RGB", masker.size, "white")
        laag.paste(inkt, mask=masker)
        # snippers in dezelfde inkt over het hele vak: verbergen de vorm van het woord voor het blote oog
        d = ImageDraw.Draw(laag)
        for _ in range(snippers):
            x, y = rng.uniform(0, BREEDTE), rng.uniform(0, HOOGTE)
            d.line([(x, y), (x + rng.uniform(-40, 40), y + rng.uniform(-40, 40))], fill=inkt, width=rng.randint(15, 45))
        # inkt op inkt: vermenigvuldigen, zoals bij drukken
        beeld = ImageChops.multiply(beeld, laag)
        if i < len(woorden):
            maskers.append(masker)
    return beeld, maskers


def maak(params: dict):
    """Geeft de woorden per vak en per vak (afbeelding, maskers) terug. Elk vak volgt de kleurcode."""
    volgorde = params["volgorde"]
    onbekend = [f for f in volgorde if f not in FILTERS]
    if onbekend or not volgorde or len(set(volgorde)) != len(volgorde):
        raise ValueError(f"volgorde moet elke kleur hoogstens één keer bevatten, uit: {', '.join(FILTERS)} (kreeg {volgorde})")
    woorden = [w.upper() for w in params["antwoord"].replace("-", " ").split()]
    if not woorden:
        raise ValueError("Het antwoord mag niet leeg zijn")
    n = len(volgorde)
    per_vak = [woorden[i:i + n] for i in range(0, len(woorden), n)]
    rng = random.Random(params["seed"])
    return per_vak, [maak_vak(ws, volgorde, params["snippers"], rng) for ws in per_vak]


def door_filter(beeld: Image.Image, filter_: str) -> Image.Image:
    """Wat je ziet door een ideale filter: enkel het kanaal van die kleur, in grijstinten."""
    return beeld.getchannel(FILTERS[filter_][1])


def teken_kleurcode(p: Pdf, volgorde: list[str], uitleg: str, t: dict) -> None:
    p.kop(t["kleurcode"])
    p.regel(uitleg)
    r = 0.9 * cm
    p.ruimte(2 * r + 4)
    for i, f in enumerate(volgorde):
        x = MARGE + r + i * 3.2 * r
        p.c.setFillColorRGB(*FILTERS[f][2])
        p.c.circle(x, p.y + r, r, stroke=0, fill=1)
        if i < len(volgorde) - 1:  # pijltje naar de volgende kleur
            p.c.setFillGray(0.3)
            p.c.setStrokeGray(0.3)
            p.c.line(x + 1.25 * r, p.y + r, x + 1.9 * r, p.y + r)
            p.c.drawString(x + 1.85 * r, p.y + r - 4, ">")
    p.c.setFillGray(0)
    p.c.setStrokeGray(0)
    p.ruimte(10)


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord, volgorde = params["antwoord"], params["volgorde"]
    per_vak, vakken = maak(params)
    meer = len(vakken) > 1
    uitleg = t["kleurcode_vakken"] if meer else t["kleurcode_uitleg"]

    # alle vakken onder elkaar in één afbeelding, voor de beeldbewerker of om groot te printen
    marge = 40
    blad = Image.new("RGB", (BREEDTE, len(vakken) * (HOOGTE + marge) - marge), "white")
    for i, (beeld, _) in enumerate(vakken):
        blad.paste(beeld, (0, i * (HOOGTE + marge)))
    blad.save(uit / "kleuren.png")

    breedte = W - 2 * MARGE
    hoogte = breedte * HOOGTE / BREEDTE
    with tempfile.TemporaryDirectory() as tmp:
        p = Pdf(uit / "deelnemer.pdf", t["titel"])
        p.regel(t["intro"])
        p.regel(t["opdracht_vakken"] if meer else t["opdracht"])
        for i, (beeld, _) in enumerate(vakken, 1):
            pad = Path(tmp) / f"vak{i}.png"
            beeld.save(pad)
            if p.y - hoogte - (30 if meer else 0) < MARGE + 2 * cm:
                p.pagina(t["titel"])
            if meer:
                p.kop(t["vak"].format(n=i))
            p.ruimte(hoogte + 6)
            p.c.drawImage(str(pad), MARGE, p.y, breedte, hoogte)
            p.c.rect(MARGE, p.y, breedte, hoogte)
            p.ruimte(10)
        if params["kleurcode_op_blad"]:
            if p.y - 4 * cm < MARGE + 1 * cm:
                p.pagina(t["titel"])
            teken_kleurcode(p, volgorde, uitleg, t)
        p.opslaan()

        # de kleurcode apart, om uit te delen als beloning van een andere uitdaging
        k = Pdf(uit / "kleurcode.pdf", t["kleurcode"])
        teken_kleurcode(k, volgorde, uitleg, t)
        k.opslaan()

        regels, nr = [], 1
        for i, ws in enumerate(per_vak, 1):
            for f, w in zip(volgorde, ws):
                regels.append(t["per_filter"].format(n=nr, vak=t["vak"].format(n=i), filter=t["filters"][f], woord=w))
                nr += 1
        b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, [t["oplossing"]] + regels, t["hints"], params["taal"])
        b.kop(t["zicht"])
        klein = breedte * 0.3
        kh = klein * HOOGTE / BREEDTE
        for i, ((beeld, _), ws) in enumerate(zip(vakken, per_vak), 1):
            if b.y - kh - 30 < MARGE + 1 * cm:
                b.pagina(t["titel"])
            b.regel(t["vak"].format(n=i), grootte=10)
            b.ruimte(kh)
            # de filters van een vak naast elkaar
            for j, f in enumerate(volgorde[:len(ws)]):
                pad = Path(tmp) / f"zicht{i}-{j}.png"
                door_filter(beeld, f).save(pad)
                b.c.drawImage(str(pad), MARGE + j * (klein + 0.3 * cm), b.y, klein, kh)
            b.ruimte(18)
        b.opslaan()

    if params["met_beeldbewerker"]:
        gebruik(uit, params["taal"], "beeldbewerker", opties={"beeldbewerker": {"afbeelding": str(uit / "kleuren.png")}})
    return antwoord


def check(params: dict) -> None:
    """Door elke filter moet zijn woord duidelijk donkerder zijn dan de rest van het vak."""
    _, vakken = maak(params)
    for beeld, maskers in vakken:
        for f, masker in zip(params["volgorde"], maskers):
            zicht = door_filter(beeld, f)
            woord = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m > 128]
            rest = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m == 0]
            verschil = sum(rest) / len(rest) - sum(woord) / len(woord)
            assert verschil > 120, f"te weinig contrast door de {f} filter ({verschil:.0f})"
