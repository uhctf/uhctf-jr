"""Laptopmap van een event: landingspagina, kluis, decoder en de digitale versies van de uitdagingen. Alles opent zonder internet vanaf schijf.

Een event krijgt een laptopmap als er een [laptop]-tabel in events/<event>/event.toml staat. Zie CONTRIBUTING.md.
"""
import hashlib
import html
import json
import re
import shutil
import unicodedata
from datetime import date
from pathlib import Path

from . import digitaal
from .paths import ToolError

SJABLONEN = Path(__file__).parent / "laptop_sjablonen"
LOGO = Path(__file__).resolve().parents[2] / "assets" / "logo.png"
INTRO = "Welkom, geheim agent! Los opdrachten op en typ de antwoorden in de kluis. Open {nodig} sloten."


def normaliseer(tekst: str) -> str:
    """Hoofdletters, spaties, accenten en leestekens tellen niet mee. Moet gelijk zijn aan de JavaScript in kluis.html."""
    tekst = unicodedata.normalize("NFD", tekst)
    tekst = "".join(ch for ch in tekst if unicodedata.category(ch) != "Mn")
    return re.sub(r"[^a-z0-9]", "", tekst.lower())


def hash_antwoord(salt: str, antwoord: str) -> str:
    return hashlib.sha256(f"{salt}:{normaliseer(antwoord)}".encode()).hexdigest()


def antwoorden_van(antwoord: str | None) -> list[str]:
    """Alle geldige antwoorden uit wat een generator teruggeeft.

    Bij varianten geeft een generator meerdere regels terug, zoals 'variant 1: vissen' of 'Lotte: milan2015'.
    Het deel na de eerste ': ' is het antwoord.
    """
    if not antwoord:
        return []
    regels = [r.split(": ", 1)[-1].strip() for r in antwoord.splitlines()]
    return [r for r in regels if normaliseer(r)]


json_in_script = digitaal.json_in_script


def vul(sjabloon: str, waarden: dict[str, str]) -> str:
    tekst = (SJABLONEN / sjabloon).read_text()
    for sleutel, waarde in waarden.items():
        tekst = tekst.replace("{{" + sleutel + "}}", waarde)
    return tekst


def nav_html(pad: str = "") -> str:
    """Balk bovenaan elke pagina: terug naar de startpagina en het logo. 'pad' is het relatieve pad naar de laptopmap ('' of '../')."""
    terug = f'<a class="terug" href="{pad}index.html">&larr; Startpagina</a>' if pad else ""
    return f'<nav class="top">{terug}<img src="{pad}logo.png" alt="UHCTF Jr"></nav>'


def decoder_met_terugknop(pad: Path) -> None:
    """De decoder is een zelfstandig hulpmiddel zonder link naar een startpagina. In de laptopmap voegen we die hier toe."""
    tekst = pad.read_text()
    if "</head>" not in tekst or "<main>" not in tekst:
        raise ToolError("decoder/index.html heeft een onverwachte opbouw: kan geen terugknop toevoegen")
    standaard = '(navigator.language.startsWith("en") ? "en" : "nl")'
    if standaard not in tekst:
        raise ToolError("decoder/index.html heeft een onverwachte opbouw: kan de standaardtaal niet op Nederlands zetten")
    tekst = tekst.replace(standaard, '"nl"')  # deze map is voor een Nederlandstalig event
    stijl = '<link rel="stylesheet" href="../stijl.css">\n</head>'  # de huisstijl van de laptopmap, na de eigen stijl van de decoder
    pad.write_text(tekst.replace("</head>", stijl, 1).replace("<main>", "<main>\n  " + nav_html("../"), 1))


# Pictogrammen voor de tegels op de startpagina (48x48, lijn in het donkergrijs van het logo)
_S = 'viewBox="0 0 48 48" fill="none" stroke="#222" stroke-width="3.5" stroke-linecap="square" stroke-linejoin="miter" aria-hidden="true"'
ICONEN = {
    "romeinse-geheimen": f'<svg {_S}><rect x="6" y="6" width="36" height="36"/><rect x="15" y="15" width="18" height="18"/><path d="M24 6v9M24 33v9M6 24h9M33 24h9"/></svg>',
    "wachtwoord-mastermind": f'<svg {_S}><rect x="8" y="8" width="12" height="12" fill="#fff"/><rect x="28" y="8" width="12" height="12" fill="#222"/><rect x="8" y="28" width="12" height="12" fill="#222"/><rect x="28" y="28" width="12" height="12" fill="#fff"/></svg>',
    "wie-is-de-hacker": f'<svg {_S}><rect x="7" y="7" width="23" height="23" fill="#fff"/><path d="M28 28l14 14"/><path d="M13 18h11"/></svg>',
    "phishing-of-echt": f'<svg {_S}><path d="M5 24l10-10h14l8 10-8 10H15z" fill="#fff"/><path d="M37 24l7-8v16z" fill="#fff"/><path d="M14 22h4v4h-4z" fill="#222"/></svg>',
    "laag-na-laag": f'<svg {_S}><path d="M24 6l18 9-18 9-18-9z" fill="#fff"/><path d="M6 24l18 9 18-9"/><path d="M6 33l18 9 18-9"/></svg>',
    "doolhof": f'<svg {_S}><path d="M6 6h36v36H6zM6 18h24M18 30h24M18 18v12"/></svg>',
    "woordzoeker": f'<svg {_S}><path d="M6 6h36v36H6zM18 6v36M30 6v36M6 18h36M6 30h36"/></svg>',
    "schatkaart": f'<svg {_S}><path d="M6 10l12-4 12 4 12-4v32l-12 4-12-4-12 4z" fill="#fff"/><path d="M18 6v32M30 10v32M20 20l8 8M28 20l-8 8"/></svg>',
    "decoder": f'<svg {_S}><path d="M16 14L6 24l10 10M32 14l10 10-10 10M27 10l-6 28"/></svg>',
    "kluis": f'<svg {_S}><rect x="6" y="8" width="36" height="32" fill="#fff"/><rect x="17" y="17" width="14" height="14" transform="rotate(45 24 24)"/><path d="M24 12v4M24 32v4M12 24h4M32 24h4"/></svg>',
}
ICOON_STANDAARD = f'<svg {_S}><path d="M10 10h12v6h8v-6h8v12h-6v8h6v8H10z" fill="#fff"/></svg>'


KLUISKNOP = '<a class="kluislink" href="../kluis/index.html"><button class="primair" type="button">Naar de kluis &rarr;</button></a>'


def maak_pagina(tekst: str) -> str:
    """Zet een digitale pagina van een uitdaging in de laptopmap: terug-link, knop naar de kluis en het pad naar de decoder."""
    return (tekst.replace("<!--NAV-->", nav_html("../")).replace("<!--KLUIS-->", KLUISKNOP)
            .replace('"decoder/index.html', '"../decoder/index.html'))


def bouw(eventnaam: str, cfg: dict | None, resultaten: list[dict], uit: Path) -> Path | None:
    """Schrijf uit/laptop/. 'resultaten': per uitdaging naam, config, antwoord, uit (de map met het gebouwde materiaal)."""
    if cfg is None:
        return None
    if any(r["naam"] == "laptop" for r in resultaten):
        raise ToolError("Een uitdaging mag niet 'laptop' heten: die naam is voor de laptopmap van het event")
    doel = uit / "laptop"
    doel.mkdir()
    shutil.copy2(SJABLONEN / "stijl.css", doel / "stijl.css")
    shutil.copy2(LOGO, doel / "logo.png")

    # kluis: de antwoorden staan enkel als hash in de pagina; een kind dat de broncode opent, leest ze dus niet zomaar
    salt = f"uhctf-{eventnaam}"
    opdrachten = []
    for r in resultaten:
        config = r["config"]
        if config.get("type") == "static":
            antwoorden = [waarde for _, waarde in config.get("vlaggen", [])]
        else:
            antwoorden = antwoorden_van(r["antwoord"])
        if antwoorden:
            opdrachten.append({"id": r["naam"], "naam": config.get("nl", {}).get("naam", r["naam"]),
                               "hashes": sorted({hash_antwoord(salt, a) for a in antwoorden})})
    nodig = int(cfg.get("nodig", 3))
    if not 1 <= nodig <= len(opdrachten):
        raise ToolError(f"event.toml, [laptop]: nodig = {nodig}, maar het event heeft {len(opdrachten)} uitdagingen met een antwoord")
    (doel / "kluis").mkdir()
    (doel / "kluis" / "index.html").write_text(vul("kluis.html", {"NAV": nav_html("../"), "DATA": json_in_script(
        {"event": eventnaam, "salt": salt, "nodig": nodig, "datum": date.today().strftime("%d-%m-%Y"), "opdrachten": opdrachten})}))

    # de decoder: één keer, voor alle pagina's
    from .shared import Resource
    Resource("decoder").build(doel / "decoder")
    decoder_met_terugknop(doel / "decoder" / "index.html")

    # digitale versies: elke uitdaging met digitaal = true levert digitaal.html (en digitaal-2.html, ... bij varianten)
    opdrachtkaarten = []
    for r in resultaten:
        gevonden = {}
        for pagina in r["uit"].glob(f"{digitaal.BESTAND.removesuffix('.html')}*.html"):
            m = re.fullmatch(r"digitaal(?:-(\d+))?\.html", pagina.name)
            if m:
                gevonden[int(m.group(1) or 1)] = pagina
        if not gevonden:
            continue
        nl = r["config"].get("nl", {})
        (doel / r["naam"]).mkdir()
        links = []
        for variant, pagina in sorted(gevonden.items()):
            naam = "index.html" if variant == 1 else f"variant-{variant}.html"
            (doel / r["naam"] / naam).write_text(maak_pagina(pagina.read_text()))
            links.append((variant, f"{r['naam']}/{naam}"))
        opdrachtkaarten.append((r["naam"], nl.get("naam", r["naam"]), nl.get("onderwerp", ""), links))

    def tegel(naam: str, href: str, titel: str, tekst: str, groot: bool = False) -> str:
        icoon = ICONEN.get(naam, ICOON_STANDAARD)
        return (f'    <a class="kaart tegel{" groot" if groot else ""}" href="{href}" data-id="{naam}"><span class="icoon">{icoon}</span>'
                f'<span><h2>{html.escape(titel)}</h2><p class="klein">{html.escape(tekst)}</p></span><span class="vink">&#10003;</span></a>')

    opdrachten = ""
    if opdrachtkaarten:
        tegels = []
        for naam, titel, tekst, links in opdrachtkaarten:
            for variant, href in links:
                tegels.append(tegel(naam, href, titel + (f" (variant {variant})" if len(links) > 1 else ""), tekst))
        opdrachten = '  <h2 class="sectie">Opdrachten op de laptop</h2>\n  <div class="raster">\n' + "\n".join(tegels) + "\n  </div>\n"
    hulp = [tegel("decoder", "decoder/index.html#t=nl", "Decoder", "Hulpmiddel voor codes."),
            tegel("kluis", "kluis/index.html", "De kluis", "Typ hier je antwoorden.", True)]
    (doel / "index.html").write_text(vul("landing.html", {
        "NAV": nav_html(), "INTRO": html.escape(cfg.get("intro", INTRO).replace("{nodig}", str(nodig))),
        "TITEL": html.escape(cfg.get("titel", eventnaam)), "OPDRACHTEN": opdrachten, "KAARTEN": "\n".join(hulp), "NODIG": str(nodig),
        "EVENT": eventnaam}))
    return doel
