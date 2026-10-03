import difflib
import importlib.util
import json
import re
import shutil
import sys
import tempfile
from pathlib import Path

import tomllib

from .paths import CHALLENGES, ROOT, ToolError

NAAM_RE = re.compile(r"^[a-z0-9][a-z0-9-]*$")
TALEN = ("nl", "en")


def alle() -> list[str]:
    return sorted(p.parent.name for p in CHALLENGES.glob("*/challenge.toml") if not p.parent.name.startswith("_"))


def toml_waarde(v) -> str:
    # JSON-strings, -getallen, -booleans en -lijsten zijn geldige TOML.
    return json.dumps(v, ensure_ascii=False)


def cast(sleutel: str, waarde, standaard):
    """Zet een tekst van de opdrachtregel om naar het type van de standaardwaarde."""
    if not isinstance(waarde, str):
        return waarde
    if isinstance(standaard, bool):
        if waarde.lower() in ("true", "ja", "1", "yes"):
            return True
        if waarde.lower() in ("false", "nee", "0", "no"):
            return False
        raise ToolError(f"'{sleutel}' verwacht ja/nee, kreeg '{waarde}'")
    if isinstance(standaard, int):
        try:
            return int(waarde)
        except ValueError:
            raise ToolError(f"'{sleutel}' verwacht een getal, kreeg '{waarde}'")
    if isinstance(standaard, list):
        return [x.strip() for x in waarde.split(",") if x.strip()]
    return waarde


class Challenge:
    def __init__(self, naam: str):
        self.naam = naam
        self.dir = CHALLENGES / naam
        if not NAAM_RE.match(naam) or not (self.dir / "challenge.toml").exists():
            tips = difflib.get_close_matches(naam, alle(), n=3)
            extra = f" Bedoelde je: {', '.join(tips)}?" if tips else f" Beschikbaar: {', '.join(alle())}"
            raise ToolError(f"Onbekende uitdaging '{naam}'.{extra}")
        self.config = tomllib.loads((self.dir / "challenge.toml").read_text())
        self.type = self.config.get("type", "static")
        if self.type not in ("static", "generated"):
            raise ToolError(f"{naam}: type moet 'static' of 'generated' zijn")

    @property
    def is_static(self) -> bool:
        return self.type == "static"

    @property
    def standaard_antwoord(self):
        return self.config.get("antwoord")

    @property
    def paden(self) -> list[str]:
        """Opties die een bestandspad zijn. In een event is zo'n pad relatief ten opzichte van de eventmap."""
        return self.config.get("paden", [])

    @property
    def zonder_vlag(self) -> bool:
        """Standaard geen vlag: de actie zelf is de opdracht (bv. een slot openen onder toezicht)."""
        return self.config.get("meta", {}).get("vlag_formaat") == "geen"

    @property
    def opties(self) -> dict:
        return self.config.get("opties", {})

    @property
    def requirements(self) -> Path:
        return self.dir / "requirements.txt"

    def geldige_sleutels(self) -> list[str]:
        sleutels = list(self.opties)
        if "antwoord" in self.config:
            sleutels.insert(0, "antwoord")
        return sleutels

    def controleer_overrides(self, overrides: dict) -> dict:
        """Valideer en cast overrides. Statische uitdagingen accepteren er geen."""
        if not overrides:
            return {}
        if self.is_static:
            raise ToolError(
                f"'{self.naam}' is een statische uitdaging en kan niet event-specifiek gebouwd worden "
                f"(gevraagd: {', '.join(overrides)}). Pas het materiaal zelf aan of maak er een gegenereerde uitdaging van.")
        geldig = self.geldige_sleutels()
        resultaat = {}
        if "taal" in overrides and str(overrides["taal"]) not in TALEN:
            raise ToolError(f"taal moet {' of '.join(TALEN)} zijn, kreeg '{overrides['taal']}'")
        for k, v in overrides.items():
            if k not in geldig:
                if k == "antwoord":
                    raise ToolError(f"'{self.naam}' heeft geen vrij antwoord (het wordt berekend). Opties: {', '.join(geldig)}")
                raise ToolError(f"'{self.naam}' kent de optie '{k}' niet. Opties: {', '.join(geldig)}")
            standaard = self.config["antwoord"] if k == "antwoord" else self.opties[k]
            resultaat[k] = cast(k, v, standaard)
        if "antwoord" in resultaat and not str(resultaat["antwoord"]).strip():
            raise ToolError("Het antwoord mag niet leeg zijn")
        return resultaat

    def parameters(self, overrides: dict) -> dict:
        params = dict(self.opties)
        if "antwoord" in self.config:
            params["antwoord"] = self.config["antwoord"]
        params.update(overrides)
        return params

    def _module(self):
        pad = self.dir / "generate.py"
        if not pad.exists():
            raise ToolError(f"{self.naam}: generate.py ontbreekt")
        sys.path.insert(0, str(ROOT / "tools"))
        spec = importlib.util.spec_from_file_location(f"challenge_{self.naam.replace('-', '_')}", pad)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ModuleNotFoundError as e:
            raise ToolError(f"Ontbrekende vereiste '{e.name}'. Installeer met: ./jr install {self.naam}")
        return module

    def build(self, uit: Path, overrides: dict | None = None) -> str | None:
        """Bouw de uitdaging in map 'uit'. Geeft het antwoord terug (None bij statisch)."""
        overrides = self.controleer_overrides(overrides or {})
        uit.mkdir(parents=True, exist_ok=True)
        if self.is_static:
            materiaal = self.config.get("materiaal", [])
            if not materiaal:
                raise ToolError(f"{self.naam}: 'materiaal' ontbreekt in challenge.toml")
            for deel in materiaal:
                bron = self.dir / deel
                if not bron.exists():
                    raise ToolError(f"{self.naam}: materiaal '{deel}' bestaat niet")
                doel = uit / bron.name
                shutil.copytree(bron, doel, dirs_exist_ok=True) if bron.is_dir() else shutil.copy2(bron, doel)
            return None
        try:
            return self._module().generate(self.parameters(overrides), uit)
        except (ValueError, AssertionError) as e:  # ongeldige invoer: toon een nette fout zonder traceback
            raise ToolError(f"{self.naam}: {e}")

    def check(self) -> str:
        """Bouw met standaardwaarden in een tijdelijke map en voer de zelftest van de generator uit."""
        if self.is_static:
            with tempfile.TemporaryDirectory() as tmp:
                self.build(Path(tmp))
                tekst = "".join(
                    f.read_text(errors="ignore") for f in Path(tmp).rglob("*") if f.is_file() and f.suffix in (".html", ".json", ".js", ".txt", ".md", ".py"))
            ontbreekt = [v for _, v in self.config.get("vlaggen", []) if v not in tekst]
            if ontbreekt:
                raise ToolError(f"{self.naam}: vlag(gen) {ontbreekt} staan niet in het materiaal")
            return "statisch: materiaal aanwezig, vlaggen gevonden"
        module = self._module()
        params = self.parameters({})
        with tempfile.TemporaryDirectory() as tmp:
            module.generate(params, Path(tmp))
        if hasattr(module, "check"):
            module.check(params)
            return "gebouwd en zelftest geslaagd"
        return "gebouwd (geen zelftest)"
