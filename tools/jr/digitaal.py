"""Digitale versie van een uitdaging: één zelfstandige webpagina (digitaal.html) die offline vanaf schijf werkt.

Een generator schrijft die pagina als 'digitaal' in zijn opties aanstaat:

    if params.get("digitaal"):
        schrijf(uit, "Doolhof", "uitleg", "<div id='x'></div>", Path(__file__).parent / "digitaal.js", data, hints)

De pagina bevat de puzzel (DATA, JSON) en het script van de uitdaging. Standalone staat de pagina los in de uitvoermap;
in de laptopmap van een event vervangt jr.laptop de markers <!--NAV--> en <!--KLUIS--> door een terug-link en een knop naar de kluis.
"""
import json
from pathlib import Path

SJABLONEN = Path(__file__).parent / "laptop_sjablonen"
BESTAND = "digitaal.html"

# Hulp voor alle digitale pagina's: hints die je een voor een toont en een kleine querySelector.
GEMEENSCHAPPELIJK = """
const $ = (id) => document.getElementById(id);
function maakHints(hints) {
  const knop = $("hint-knop");
  let getoond = 0;
  if (!hints.length) { $("hint-kaart").hidden = true; return; }
  knop.addEventListener("click", () => {
    const p = document.createElement("div");
    p.className = "hint";
    p.textContent = (getoond + 1) + ". " + hints[getoond];
    $("hints").appendChild(p);
    if (++getoond >= hints.length) knop.disabled = true;
  });
}
maakHints(HINTS);
"""



def json_in_script(data) -> str:
    """JSON om in een <script> te zetten: een '</' in de tekst mag de scripttag niet afsluiten."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def schrijf(uit: Path, titel: str, intro: str, body: str, script: Path, data: dict, hints: list[str], css: str = "",
            naam: str = BESTAND) -> Path:
    """Schrijf uit/<naam> (standaard digitaal.html). 'body' en 'intro' zijn HTML, 'script' is het bestand met de logica van de uitdaging.
    Heeft een uitdaging varianten, dan heten de extra pagina's digitaal-2.html, digitaal-3.html, enz."""
    stijl = (SJABLONEN / "stijl.css").read_text() + css
    pagina = f"""<!doctype html>
<html lang="nl">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{titel}</title>
  <style>
{stijl}
  </style>
</head>
<body>
<main>
  <!--NAV-->
  <h1>{titel}</h1>
  <p>{intro}</p>
{body}
  <div class="voet" id="hint-kaart">
    <div id="hints"></div>
    <button id="hint-knop" type="button">Hint</button>
    <!--KLUIS-->
  </div>
</main>
<script>
const DATA = {json_in_script(data)};
const HINTS = {json_in_script(hints)};
{GEMEENSCHAPPELIJK}
{script.read_text()}
</script>
</body>
</html>
"""
    pad = uit / naam
    pad.write_text(pagina)
    return pad
