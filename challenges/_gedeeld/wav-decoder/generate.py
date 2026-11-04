"""WAV-decoder: kopieert index.html en bouwt optioneel een standaardgeluid in (als base64)."""
import base64
import json
import re
import tempfile
from pathlib import Path

HIER = Path(__file__).parent
MAX_BYTES = 12 * 1024 * 1024


def bouw_html(params: dict) -> str:
    html = (HIER / "index.html").read_text()
    pad = params.get("geluid", "")
    b64 = ""
    if pad:
        p = Path(pad)
        if not p.is_file():
            raise ValueError(f"geluid '{pad}' bestaat niet")
        data = p.read_bytes()
        if data[:4] != b"RIFF" or data[8:12] != b"WAVE":
            raise ValueError(f"geluid '{pad}' is geen WAV-bestand")
        if len(data) > MAX_BYTES:
            raise ValueError(f"geluid is {len(data) // 1024 // 1024} MB; verklein het tot maximaal {MAX_BYTES // 1024 // 1024} MB")
        b64 = base64.b64encode(data).decode()
    html, n = re.subn(r'const STANDAARD_GELUID = ".*?";', lambda m: f"const STANDAARD_GELUID = {json.dumps(b64)};", html, count=1)
    assert n == 1, "index.html mist de constante STANDAARD_GELUID"
    return html


def generate(params: dict, uit: Path) -> None:
    uit.mkdir(parents=True, exist_ok=True)
    (uit / "index.html").write_text(bouw_html(params))


def check(params: dict) -> None:
    """Een ingebouwd geluid komt in de pagina terecht en zonder geluid blijft de constante leeg."""
    import struct
    import wave
    with tempfile.TemporaryDirectory() as tmp:
        pad = Path(tmp) / "x.wav"
        with wave.open(str(pad), "wb") as w:
            w.setnchannels(1)
            w.setsampwidth(2)
            w.setframerate(8000)
            w.writeframes(struct.pack("<100h", *range(100)))
        html = bouw_html({**params, "geluid": str(pad)})
    assert re.search(r'const STANDAARD_GELUID = "UklGR', html), "WAV niet ingebouwd (RIFF in base64 verwacht)"
    assert 'const STANDAARD_GELUID = "";' in bouw_html({**params, "geluid": ""})
