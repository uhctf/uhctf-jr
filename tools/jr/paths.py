from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CHALLENGES = ROOT / "challenges"
EVENTS = ROOT / "events"
TEMPLATE = ROOT / "template"
VENV = ROOT / ".venv"


class ToolError(Exception):
    """Fout die netjes aan de gebruiker getoond wordt."""
