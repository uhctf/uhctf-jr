import shutil
from datetime import date
from pathlib import Path

import tomllib

from .challenge import Challenge, toml_waarde
from .paths import EVENTS, ToolError

KOP = "# Uitdagingen voor dit event. Elke tabel is een uitdaging; sleutels overschrijven de standaardwaarden.\n"


def alle() -> list[str]:
    return sorted(p.name for p in EVENTS.iterdir() if p.is_dir())


class Event:
    def __init__(self, naam: str):
        from .challenge import NAAM_RE
        self.naam = naam
        self.dir = EVENTS / naam
        if not NAAM_RE.match(naam) or not self.dir.is_dir():
            raise ToolError(f"Onbekend event '{naam}'. Beschikbaar: {', '.join(alle())}. Nieuw event: ./jr event new {naam}")
        self.bestand = self.dir / "uitdagingen.toml"

    def lees(self) -> dict[str, dict]:
        if not self.bestand.exists():
            return {}
        return tomllib.loads(self.bestand.read_text())

    def schrijf(self, data: dict[str, dict]) -> None:
        delen = [KOP]
        for naam, overrides in data.items():
            delen.append(f"\n[{naam}]\n")
            for k, v in overrides.items():
                delen.append(f"{k} = {toml_waarde(v)}\n")
        self.bestand.write_text("".join(delen))

    def add(self, naam: str, overrides: dict | None = None) -> dict:
        ch = Challenge(naam)
        overrides = ch.controleer_overrides(overrides or {})
        for sleutel in ch.paden:
            if overrides.get(sleutel) and not (self.dir / overrides[sleutel]).is_file():
                raise ToolError(f"'{sleutel}': bestand '{overrides[sleutel]}' niet gevonden in {self.dir.relative_to(EVENTS.parent)}")
        data = self.lees()
        data[naam] = overrides
        self.schrijf(data)
        return overrides

    def remove(self, naam: str) -> None:
        data = self.lees()
        if naam not in data:
            raise ToolError(f"'{naam}' staat niet in {self.naam}")
        del data[naam]
        self.schrijf(data)

    def uitdagingen(self) -> list[tuple[Challenge, dict]]:
        data = self.lees()
        if not data:
            raise ToolError(f"{self.naam} heeft nog geen uitdagingen. Voeg toe met: ./jr event add {self.naam} <uitdaging>")
        # Valideert meteen: onbekende uitdagingen of overrides op statische uitdagingen falen hier.
        resultaat = []
        for naam, overrides in data.items():
            ch = Challenge(naam)
            resultaat.append((ch, ch.controleer_overrides(overrides)))
        return resultaat

    def _pad_overrides(self, ch: Challenge, overrides: dict) -> dict:
        """Maak bestandspaden in de overrides absoluut, ten opzichte van de eventmap."""
        resultaat = dict(overrides)
        for sleutel in ch.paden:
            if resultaat.get(sleutel):
                pad = Path(resultaat[sleutel])
                resultaat[sleutel] = str(pad if pad.is_absolute() else self.dir / pad)
        return resultaat

    def _antwoorden_pdf(self, pad: Path, rijen: list[tuple[str, str, str]]) -> None:
        from .pdf import Pdf
        p = Pdf(pad, f"Antwoorden: {self.naam}")
        p.regel(f"Event: {self.naam}. Gemaakt op {date.today().isoformat()}.")
        p.regel("Alleen voor begeleiders: niet uitdelen aan deelnemers.", 12)
        p.ruimte(8)
        p.tabel(("Uitdaging", "Antwoord", "Bron"), rijen, (3, 5, 2))
        p.opslaan()

    def build(self) -> Path:
        items = self.uitdagingen()
        uit = self.dir / "out"
        if uit.exists():
            shutil.rmtree(uit)
        uit.mkdir()
        rijen = []
        for ch, overrides in items:
            print(f"- {ch.naam} ...", end=" ", flush=True)
            antwoord = ch.build(uit / ch.naam, self._pad_overrides(ch, overrides))
            print("ok")
            titel = ch.config.get("nl", {}).get("naam", ch.naam)
            if ch.is_static:
                vlaggen = "\n".join(f"{label}: {waarde}" for label, waarde in ch.config.get("vlaggen", []))
                rijen.append((titel, vlaggen or "-", "vast materiaal"))
            else:
                bron = "event" if overrides else "standaard"
                rijen.append((titel, antwoord if antwoord is not None else "(geen vlag)", bron))
        self._antwoorden_pdf(uit / "ANTWOORDEN.pdf", rijen)
        return uit


def nieuw(naam: str, template: Path) -> Path:
    from .challenge import NAAM_RE
    if not NAAM_RE.match(naam):
        raise ToolError("Naam moet uit kleine letters, cijfers en koppeltekens bestaan")
    doel = EVENTS / naam
    if doel.exists():
        raise ToolError(f"Event '{naam}' bestaat al")
    doel.mkdir(parents=True)
    tekst = template.read_text().replace("<+Naam+>", naam.replace("-", " ").title())
    (doel / "README.md").write_text(tekst)
    (doel / "uitdagingen.toml").write_text(KOP)
    return doel
