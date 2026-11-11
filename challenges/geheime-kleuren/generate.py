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
# Volle inkten: zo donker mogelijk door de juiste filter. Cyaan (voor rood) is ook zonder filter goed zichtbaar,
# daarom is rood standaard de kleur van het afleidingswoord.
# Printers en mica's verschillen: maak altijd een testafdruk.
FILTERS = {
    "rood": ((0, 255, 255), 0, (0.9, 0.1, 0.1)),
    "groen": ((255, 0, 255), 1, (0.1, 0.65, 0.2)),
    "blauw": ((255, 255, 0), 2, (0.1, 0.3, 0.9)),
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
        "afleiding": "Afleiding (zichtbaar zonder filter en door de {filter} filter): {woorden}. Dit is niet het antwoord.",
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
        "afleiding": "Red herring (visible without a filter and through the {filter} filter): {woorden}. This is not the answer.",
        "filters": {"rood": "red", "groen": "green", "blauw": "blue"},
        "hints": ["Look through each filter. Do you see something different each time?",
                  "Each filter colour shows one word. Write down which word goes with which colour.",
                  "Put the words in the order of the colour code."],
    },
}


def lettertype(grootte: int):
    return ImageFont.load_default(size=grootte)


def driehoekjes(masker: Image.Image, cel: int, rng: random.Random) -> Image.Image:
    """Bouw de vorm opnieuw op uit driehoekjes: elk vierkantje van het raster wordt in twee gedeeld, en een driehoekje
    blijft als zijn midden in de vorm ligt. Tussen de driehoekjes blijft een smalle witte rand."""
    uit = Image.new("L", masker.size, 0)
    d = ImageDraw.Draw(uit)
    rand = max(1, cel // 12)
    # elk woord een eigen verschuiving van het raster, zodat de randen van verschillende woorden niet samenvallen
    dx, dy = rng.randrange(cel), rng.randrange(cel)
    for y in range(-dy, masker.height, cel):
        for x in range(-dx, masker.width, cel):
            a, b, c, e = (x, y), (x + cel, y), (x + cel, y + cel), (x, y + cel)
            # willekeurige diagonaal, zodat het geen saai patroon wordt
            for drie in ([a, b, c], [a, c, e]) if rng.random() < 0.5 else ([a, b, e], [b, c, e]):
                mx, my = sum(p[0] for p in drie) / 3, sum(p[1] for p in drie) / 3
                if 0 <= mx < masker.width and 0 <= my < masker.height and masker.getpixel((int(mx), int(my))) > 128:
                    # iets kleiner maken naar het midden toe: zo blijft er een rand tussen de driehoekjes
                    krimp = [(px + (mx - px) * rand / cel * 2, py + (my - py) * rand / cel * 2) for px, py in drie]
                    d.polygon(krimp, fill=255)
    return uit


def woordmasker(woord: str, vorm: str, rng: random.Random) -> Image.Image:
    """Het woord, groot, een beetje verschoven en gedraaid, zodat de woorden niet netjes op elkaar liggen."""
    grootte = 450
    while lettertype(grootte).getlength(woord) > BREEDTE * 0.85:
        grootte -= 10
    masker = Image.new("L", (BREEDTE, HOOGTE), 0)
    midden = (BREEDTE / 2 + rng.uniform(-80, 80), HOOGTE / 2 + rng.uniform(-HOOGTE / 10, HOOGTE / 10))
    ImageDraw.Draw(masker).text(midden, woord, fill=255, font=lettertype(grootte), anchor="mm",
                                stroke_width=max(4, grootte // 18), stroke_fill=255)
    if vorm == "driehoekjes":
        # voor het draaien, zodat het raster van driehoekjes mee draait en per woord een andere hoek heeft
        masker = driehoekjes(masker, max(10, grootte // 18), rng)
    return masker.rotate(rng.uniform(-10, 10), resample=Image.BICUBIC, center=midden)


def tint(inkt: tuple, sterkte: float) -> tuple:
    """Bleker versie van een inkt: 1 = volle inkt, 0 = papier."""
    return tuple(round(255 - (255 - c) * sterkte) for c in inkt)


def maak_vak(lagen: list[tuple[str, str | None, float]], params: dict, rng: random.Random):
    """Eén vak met per (kleur, woord, sterkte) een laag in de inkt van die kleur; woord None = enkel blokjes.
    Geeft de afbeelding en per laag het masker (None zonder woord) terug."""
    beeld = Image.new("RGB", (BREEDTE, HOOGTE), "white")
    maskers = []
    for f, woord, sterkte in lagen:
        inkt = FILTERS[f][0]
        masker = woordmasker(woord, params["vorm"], rng) if woord else Image.new("L", (BREEDTE, HOOGTE), 0)
        laag = Image.new("RGB", masker.size, "white")
        # blokjes in een blekere versie van dezelfde inkt: met het blote oog een wirwar die de vorm van het woord verbergt,
        # door de filter lichtgrijs naast het zwarte woord
        d = ImageDraw.Draw(laag)
        for _ in range(params["snippers"]):
            x, y, z = rng.uniform(0, BREEDTE), rng.uniform(0, HOOGTE), rng.uniform(8, 22)
            d.rectangle([x, y, x + z, y + z * rng.uniform(0.6, 1.6)], fill=tint(inkt, rng.uniform(0.35, params["blokjes_sterkte"] / 100)))
        laag.paste(tint(inkt, sterkte), mask=masker)
        # inkt op inkt: vermenigvuldigen, zoals bij drukken
        beeld = ImageChops.multiply(beeld, laag)
        maskers.append(masker if woord else None)
    return beeld, maskers


def maak(params: dict):
    """Geeft de woorden per vak, de afleidingswoorden per vak en per vak (afbeelding, maskers) terug.
    Elk vak volgt de kleurcode; de maskers volgen de kleurcode, met het afleidingswoord (als dat er is) als laatste."""
    volgorde, kleur_afl = params["volgorde"], params["afleiding_kleur"]
    onbekend = [f for f in volgorde + [kleur_afl] if f not in FILTERS]
    if onbekend or not volgorde or len(set(volgorde)) != len(volgorde):
        raise ValueError(f"volgorde moet elke kleur hoogstens één keer bevatten, uit: {', '.join(FILTERS)} (kreeg {volgorde})")
    if params["vorm"] not in ("vol", "driehoekjes"):
        raise ValueError(f"vorm moet 'vol' of 'driehoekjes' zijn, kreeg '{params['vorm']}'")
    woorden = [w.upper() for w in params["antwoord"].replace("-", " ").split()]
    afleiding = [w.upper() for w in params["afleiding"].replace("-", " ").split()]
    if not woorden:
        raise ValueError("Het antwoord mag niet leeg zijn")
    if afleiding and kleur_afl in volgorde:
        raise ValueError(f"afleiding_kleur '{kleur_afl}' staat ook in de volgorde; kies een kleur die geen echt woord toont")
    n = len(volgorde)
    per_vak = [woorden[i:i + n] for i in range(0, len(woorden), n)]
    if len(afleiding) > len(per_vak):
        raise ValueError(f"{len(afleiding)} afleidingswoorden maar {len(per_vak)} vakken: hoogstens één afleidingswoord per vak")
    afl_per_vak = [afleiding[i] if i < len(afleiding) else None for i in range(len(per_vak))]
    rng = random.Random(params["seed"])
    vakken = []
    for ws, afl in zip(per_vak, afl_per_vak):
        # elke kleur krijgt een laag, ook zonder woord, zodat elk vak even druk is
        lagen = [(f, ws[i] if i < len(ws) else None, params["woord_sterkte"] / 100) for i, f in enumerate(volgorde)]
        if afleiding:
            # de afleiding hoeft enkel zonder filter op te vallen; bleker, zodat ze de echte woorden niet zwart maakt
            lagen.append((kleur_afl, afl, params["afleiding_sterkte"] / 100))
        vakken.append(maak_vak(lagen, params, rng))
    return per_vak, afl_per_vak, vakken


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
    per_vak, afl_per_vak, vakken = maak(params)
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
        if any(afl_per_vak):
            regels.append(t["afleiding"].format(filter=t["filters"][params["afleiding_kleur"]],
                                                woorden=", ".join(w for w in afl_per_vak if w)))
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
    """Door elke filter moet zijn woord duidelijk donkerder zijn dan de rest van het vak (de afleiding telt niet mee)."""
    _, _, vakken = maak(params)
    for beeld, maskers in vakken:
        for f, masker in zip(params["volgorde"], maskers):
            if masker is None:
                continue
            zicht = door_filter(beeld, f)
            woord = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m > 128]
            rest = [v for v, m in zip(zicht.getdata(), masker.getdata()) if m == 0]
            verschil = sum(rest) / len(rest) - sum(woord) / len(woord)
            assert verschil > 120, f"te weinig contrast door de {f} filter ({verschil:.0f})"
