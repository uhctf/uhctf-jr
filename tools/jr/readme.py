"""Genereert README.md (en optioneel README.en.md) van elke uitdaging uit challenge.toml, plus het overzicht."""
import json
import tempfile
from pathlib import Path

from . import shared, venv
from .challenge import Challenge, alle
from .paths import CHALLENGES, ToolError

GEGENEREERD = {
    "nl": "<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->",
    "en": "<!-- This file is generated from challenge.toml. Edit challenge.toml and run ./jr readme. -->",
}
L = {
    "nl": {"toon": "TOON", "beschrijving": "Beschrijving", "opzet": "Opzet", "standaard": "standaard",
           "vlag_antwoord": "het antwoord zelf (hoofdletterongevoelig)",
           "vlag_geen": "geen vlag; de opdracht zelf is de actie",
           "genereer": "Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:",
           "event": "Voor een event met een eigen antwoord:",
           "event_berekend": "Voor een event met andere opties:",
           "uitvoer": "De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).",
           "opties": "Opties (standaardwaarde):", "vereisten": "Extra vereiste: installeer met",
           "statisch": "Dit is een statische uitdaging: het materiaal staat vast en er is geen event-specifieke versie. "
                       "`./jr event build` kopieert {materiaal} ongewijzigd.",
           "overzicht_kop": "Herbruikbare uitdagingen. Eén map per uitdaging; elke README wordt gegenereerd uit `challenge.toml`.",
           "kolommen": ("Uitdaging", "Type", "Formaat", "Leeftijd", "Duur", "Onderwerp"),
           "types": {"generated": "gegenereerd", "static": "statisch"},
           "overzicht_voet": "Gegenereerde uitdagingen bouw je met `./jr build <naam>`; zie [CONTRIBUTING.md](../CONTRIBUTING.md). "
                             "Statische uitdagingen hebben vast materiaal.",
           "gedeeld": "Gedeeld materiaal staat in [_gedeeld/](_gedeeld/)."},
    "en": {"toon": "SHOW", "beschrijving": "Description", "opzet": "Setup", "standaard": "default",
           "vlag_antwoord": "the answer itself (case-insensitive)",
           "vlag_geen": "no flag; the action itself is the task",
           "genereer": "This is a generated challenge. Build with the default values:",
           "event": "For an event with its own answer:",
           "event_berekend": "For an event with different options:",
           "uitvoer": "The output contains at least `deelnemer.pdf` (hand out) and `begeleider.pdf` (answer, solution, hints).",
           "opties": "Options (default value):", "vereisten": "Extra requirement: install with",
           "statisch": "This is a static challenge: the material is fixed and there is no event-specific version. "
                       "`./jr event build` copies {materiaal} unchanged.",
           "kolommen": ("Challenge", "Type", "Format", "Age", "Duration", "Topic"),
           "types": {"generated": "generated", "static": "static"}},
}


def talen(ch: Challenge) -> list[str]:
    return [t for t in ("nl", "en") if t in ch.config]


def standaardantwoord(ch: Challenge) -> str:
    """Het antwoord met standaardwaarden; bij een berekend antwoord door de generator te draaien."""
    if ch.standaard_antwoord:
        return ch.standaard_antwoord
    venv.ensure_venv()
    with tempfile.TemporaryDirectory() as tmp:
        return ch.build(Path(tmp))


def vlaggen(ch: Challenge, taal: str):
    if ch.is_static:
        lijst = ch.config.get("vlaggen")
        if not lijst:
            raise ToolError(f"{ch.naam}: 'vlaggen' ontbreekt in challenge.toml (statische uitdaging)")
        return [(l, v) for l, v in lijst]
    return [(L[taal]["standaard"], standaardantwoord(ch))]


def render(ch: Challenge, taal: str) -> str:
    t, meta, tekst = L[taal], ch.config.get("meta", {}), ch.config[taal]
    for sleutel in ("auteur", "formaat", "leeftijd", "duur"):
        if sleutel not in meta:
            raise ToolError(f"{ch.naam}: [meta] mist '{sleutel}'")
    if ch.zonder_vlag:
        vlag_fmt = t["vlag_geen"]
        vlag_blok = []
    else:
        vlag_fmt = "**uhctf{...}**" if meta.get("vlag_formaat") == "uhctf" else t["vlag_antwoord"]
        items = "\n".join(f"<li>{l}: <code>{v}</code></li>" for l, v in vlaggen(ch, taal))
        vlag_blok = ["Flag:", "", f"<details><summary>{t['toon']}</summary><ul><ul>", items, "</ul></ul></details>", ""]
    hints = "\n".join(f"{i}. {h}" for i, h in enumerate(tekst.get("hints", []), 1))

    if ch.is_static:
        auto = t["statisch"].format(materiaal=", ".join(f"`{m}/`" for m in ch.config.get("materiaal", [])))
    else:
        berekend = "antwoord" not in ch.config
        blok = [t["genereer"], f"```\n./jr build {ch.naam}\n```"]
        if berekend:
            blok += [t["event_berekend"], f"```\n./jr event add <event> {ch.naam} --set optie=waarde\n./jr event build <event>\n```"]
        else:
            blok += [t["event"], f"```\n./jr event add <event> {ch.naam} --antwoord <woord>\n./jr event build <event>\n```"]
        blok.append(t["uitvoer"])
        opties = ", ".join(f"`{k}` ({json.dumps(v, ensure_ascii=False)})" for k, v in ch.opties.items())
        if opties:
            blok.append(f"{t['opties']} {opties}.")
        if venv.has_requirements(ch.requirements):
            blok.append(f"{t['vereisten']} `./jr install {ch.naam}`.")
        auto = "\n\n".join(blok)

    delen = [
        GEGENEREERD[taal], "",
        f"# {tekst['naam']}", "",
        f"- Author: {meta['auteur']}", "",
        f"- Format: {meta['formaat']}", "",
        f"- Age: {meta['leeftijd']}", "",
        f"- Duration: {meta['duur']}", "",
        f"- Topic: {tekst['onderwerp']}", "",
        f"- Materials: {tekst['materiaal']}", "",
        f"- Flag Format: {vlag_fmt}", "",
        *vlag_blok,
        f"## {t['beschrijving']}", "", tekst["beschrijving"].strip(), "",
        "## Hints", "", hints, "",
        f"## {t['opzet']}", "",
    ]
    if tekst.get("opzet", "").strip():
        delen += [tekst["opzet"].strip(), ""]
    delen += [auto, "", "[SOLUTION.md](SOLUTION.md)", ""]
    return "\n".join(delen)


def bestanden(namen: list[str] | None = None) -> dict[Path, str]:
    """De te genereren bestanden (pad -> inhoud). Met 'namen' enkel de README's van die uitdagingen plus het overzicht."""
    uit: dict[Path, str] = {}
    rijen = []
    for naam in alle():
        ch = Challenge(naam)
        for taal in talen(ch) if namen is None or naam in namen else []:
            uit[ch.dir / ("README.md" if taal == "nl" else f"README.{taal}.md")] = render(ch, taal)
        if "nl" not in ch.config:
            raise ToolError(f"{naam}: [nl] ontbreekt in challenge.toml")
        meta = ch.config["meta"]
        rijen.append((ch.config["nl"]["naam"], naam, ch.type, meta["formaat"], meta["leeftijd"], meta["duur"],
                      ch.config["nl"]["onderwerp"]))
    for taal in ("nl", "en"):
        gedeeld = gedeeld_readme(taal)
        if gedeeld:
            uit[shared.GEDEELD / ("README.md" if taal == "nl" else "README.en.md")] = gedeeld
    t = L["nl"]
    tabel = ["| " + " | ".join(t["kolommen"]) + " |", "| " + " | ".join("---" for _ in t["kolommen"]) + " |"]
    for titel, naam, typ, fmt, leeftijd, duur, onderwerp in sorted(rijen, key=lambda r: r[1]):
        tabel.append(f"| [{titel}]({naam}/) | {t['types'][typ]} | {fmt} | {leeftijd} | {duur} | {onderwerp} |")
    uit[CHALLENGES / "README.md"] = "\n".join(
        [GEGENEREERD["nl"], "", "# Challenges", "", t["overzicht_kop"], "", *tabel, "", t["overzicht_voet"], "",
         t["gedeeld"], ""])
    return uit


GEDEELD_TEKST = {
    "nl": ("Gedeeld materiaal", "Hulpmiddelen die door meerdere uitdagingen gebruikt worden. Uitdagingen leveren ze mee in hun uitvoer, "
           "in een map met de naam van het hulpmiddel (bv. `decoder/`). Dit bestand wordt gegenereerd uit de `resource.toml` van elk hulpmiddel.",
           "Type", "gegenereerd", "statisch", "Gebruik"),
    "en": ("Shared material", "Tools used by several challenges. Challenges include them in their output, in a folder named after the tool "
           "(e.g. `decoder/`). This file is generated from each tool's `resource.toml`.",
           "Type", "generated", "static", "Usage"),
}


def gedeeld_readme(taal: str) -> str | None:
    kop, intro, _, gegen, stat, gebruik = GEDEELD_TEKST[taal]
    delen = [GEGENEREERD[taal].replace("challenge.toml", "resource.toml"), "", f"# {kop}", "", intro, ""]
    gevonden = False
    for naam in shared.alle():
        r = shared.Resource(naam)
        if taal not in r.config:
            continue
        gevonden = True
        tekst = r.config[taal]
        delen += [f"## {tekst['naam']}", "", f"- `{naam}/` ({gegen if r.type == 'generated' else stat})", "",
                  tekst["beschrijving"], "", f"{gebruik}: {tekst['gebruik']}", ""]
    return "\n".join(delen) if gevonden else None


def schrijf(namen: list[str] | None = None) -> list[Path]:
    """Schrijft de README's; geeft de gewijzigde bestanden terug."""
    gewijzigd = []
    for pad, inhoud in bestanden(namen).items():
        if not pad.exists() or pad.read_text() != inhoud:
            pad.write_text(inhoud)
            gewijzigd.append(pad)
    return gewijzigd


def verouderd() -> list[Path]:
    return [pad for pad, inhoud in bestanden().items() if not pad.exists() or pad.read_text() != inhoud]
