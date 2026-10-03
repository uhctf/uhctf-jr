"""Beeldbewerker: kopieert index.html en bouwt optioneel een standaardafbeelding en de taal in."""
import base64
import json
import re
import tempfile
from pathlib import Path

HIER = Path(__file__).parent
PNG_1X1 = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4nGP4z8DwHwAFAAH/q842iQAAAABJRU5ErkJggg==")
MIME = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".gif": "image/gif",
        ".webp": "image/webp", ".svg": "image/svg+xml"}
MAX_BYTES = 10 * 1024 * 1024


def data_url(pad: Path) -> str:
    if not pad.is_file():
        raise ValueError(f"afbeelding '{pad}' bestaat niet")
    mime = MIME.get(pad.suffix.lower())
    if not mime:
        raise ValueError(f"afbeelding moet een van {', '.join(MIME)} zijn, kreeg '{pad.suffix}'")
    data = pad.read_bytes()
    if len(data) > MAX_BYTES:
        raise ValueError(f"afbeelding is {len(data) // 1024 // 1024} MB; verklein ze tot maximaal {MAX_BYTES // 1024 // 1024} MB")
    return f"data:{mime};base64,{base64.b64encode(data).decode()}"


def bouw_html(params: dict) -> str:
    html = (HIER / "index.html").read_text()
    afbeelding = params.get("afbeelding", "")
    html, n1 = re.subn(r'const STANDAARD_AFBEELDING = ".*?";',
                       lambda m: f"const STANDAARD_AFBEELDING = {json.dumps(data_url(Path(afbeelding)) if afbeelding else '')};", html, count=1)
    html, n2 = re.subn(r'const STANDAARD_TAAL = ".*?";', lambda m: f"const STANDAARD_TAAL = {json.dumps(params['taal'])};", html, count=1)
    assert n1 == 1 and n2 == 1, "index.html mist de STANDAARD_-constanten"
    return html


def generate(params: dict, uit: Path) -> None:
    uit.mkdir(parents=True, exist_ok=True)
    (uit / "index.html").write_text(bouw_html(params))


def check(params: dict) -> None:
    """Een ingebouwde afbeelding komt in de pagina terecht en zonder afbeelding blijft de constante leeg."""
    with tempfile.TemporaryDirectory() as tmp:
        pad = Path(tmp) / "x.png"
        pad.write_bytes(PNG_1X1)
        html = bouw_html({**params, "afbeelding": str(pad)})
    assert "data:image/png;base64," in html
    assert 'const STANDAARD_AFBEELDING = "";' in bouw_html({**params, "afbeelding": ""})
