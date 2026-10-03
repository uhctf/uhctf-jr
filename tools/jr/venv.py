import os
import subprocess
import sys
import venv
from pathlib import Path

from .paths import ROOT, VENV, ToolError


def venv_python() -> Path:
    return VENV / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def in_venv() -> bool:
    return Path(sys.prefix).resolve() == VENV.resolve()


def ensure_venv() -> None:
    """Herstart in de virtuele omgeving, zodat gebruikers die niet hoeven te activeren."""
    if in_venv():
        return
    if not venv_python().exists():
        raise ToolError("Geen virtuele omgeving gevonden. Draai eerst: ./jr setup")
    os.execv(str(venv_python()), [str(venv_python()), str(ROOT / "jr"), *sys.argv[1:]])


def pip_install(requirements: Path) -> None:
    if not venv_python().exists():
        raise ToolError("Geen virtuele omgeving gevonden. Draai eerst: ./jr setup")
    subprocess.check_call([str(venv_python()), "-m", "pip", "install", "-q", "-r", str(requirements)])


def has_requirements(requirements: Path) -> bool:
    """Is er minstens één echte regel (geen commentaar) in dit requirements-bestand?"""
    if not requirements.exists():
        return False
    return any(l.strip() and not l.strip().startswith("#") for l in requirements.read_text().splitlines())


def setup() -> None:
    if not venv_python().exists():
        print(f"Virtuele omgeving maken in {VENV} ...")
        venv.create(VENV, with_pip=True)
    print("Algemene vereisten installeren ...")
    pip_install(ROOT / "requirements.txt")
    print("Klaar. Gebruik ./jr om uitdagingen te bouwen.")
