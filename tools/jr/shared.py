"""Gedeeld materiaal (challenges/_gedeeld/<naam>): hulpmiddelen die uitdagingen meeleveren.

Net als uitdagingen heeft elke gedeelde bron een resource.toml met type 'static' of 'generated'.
Gegenereerde bronnen hebben een generate.py (zelfde contract als bij uitdagingen); statische bronnen worden gekopieerd.
"""
import importlib.util
import shutil
import sys
import tempfile
from pathlib import Path

import tomllib

from .challenge import NAAM_RE, TALEN, cast
from .paths import CHALLENGES, ROOT, ToolError

GEDEELD = CHALLENGES / "_gedeeld"
BESTANDEN_NEGEREN = {"resource.toml", "generate.py", "__pycache__"}


def alle() -> list[str]:
    return sorted(p.parent.name for p in GEDEELD.glob("*/resource.toml"))


class Resource:
    def __init__(self, naam: str):
        self.naam = naam
        self.dir = GEDEELD / naam
        if not NAAM_RE.match(naam) or not (self.dir / "resource.toml").exists():
            raise ToolError(f"Onbekende gedeelde bron '{naam}'. Beschikbaar: {', '.join(alle())}")
        self.config = tomllib.loads((self.dir / "resource.toml").read_text())
        self.type = self.config.get("type", "static")

    @property
    def opties(self) -> dict:
        return self.config.get("opties", {})

    def _module(self):
        pad = self.dir / "generate.py"
        if not pad.exists():
            raise ToolError(f"{self.naam}: generate.py ontbreekt")
        sys.path.insert(0, str(ROOT / "tools"))
        spec = importlib.util.spec_from_file_location(f"gedeeld_{self.naam}", pad)
        module = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(module)
        except ModuleNotFoundError as e:
            raise ToolError(f"Ontbrekende vereiste '{e.name}'. Draai ./jr setup")
        return module

    def parameters(self, overrides: dict) -> dict:
        for k in overrides:
            if k not in self.opties:
                raise ToolError(f"'{self.naam}' kent de optie '{k}' niet. Opties: {', '.join(self.opties) or '(geen)'}")
        params = dict(self.opties)
        params.update({k: cast(k, v, self.opties[k]) for k, v in overrides.items()})
        if "taal" in params and params["taal"] not in TALEN:
            raise ToolError(f"taal moet {' of '.join(TALEN)} zijn, kreeg '{params['taal']}'")
        return params

    def build(self, uit: Path, overrides: dict | None = None) -> None:
        """Schrijf de bron in map 'uit'."""
        overrides = overrides or {}
        if self.type == "static":
            if overrides:
                raise ToolError(f"'{self.naam}' is statisch en kent geen opties")
            uit.mkdir(parents=True, exist_ok=True)
            for item in self.dir.iterdir():
                if item.name in BESTANDEN_NEGEREN:
                    continue
                shutil.copytree(item, uit / item.name, dirs_exist_ok=True) if item.is_dir() else shutil.copy2(item, uit / item.name)
            return
        try:
            self._module().generate(self.parameters(overrides), uit)
        except (ValueError, AssertionError) as e:
            raise ToolError(f"{self.naam}: {e}")

    def check(self) -> str:
        with tempfile.TemporaryDirectory() as tmp:
            self.build(Path(tmp))
        if self.type == "generated":
            module = self._module()
            if hasattr(module, "check"):
                module.check(self.parameters({}))
                return "gebouwd en zelftest geslaagd"
            return "gebouwd (geen zelftest)"
        return "statisch: bestanden aanwezig"


def gebruik(uit: Path, taal: str, *namen: str, opties: dict[str, dict] | None = None) -> None:
    """Lever gedeelde bronnen mee in de uitvoer van een uitdaging: uit/<naam>/...

    'opties' geeft per bron extra opties, bv. opties={"beeldbewerker": {"afbeelding": str(pad)}}.
    """
    for naam in namen:
        r = Resource(naam)
        extra = dict((opties or {}).get(naam, {}))
        if "taal" in r.opties:
            extra.setdefault("taal", taal)
        r.build(uit / naam, extra or None)
