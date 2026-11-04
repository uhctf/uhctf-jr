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

# Kladblok: een klein JavaScript-venster voor uitdagingen waar je moet programmeren. console.log schrijft in het uitvoervak.
KLADBLOK_CSS = """
#kb-code{min-height:220px;font-size:15px;line-height:1.45;word-break:normal;white-space:pre;overflow:auto;tab-size:2}
#kb-uit{background:var(--ink);color:#e8fffd;font-family:var(--mono);font-size:14px;padding:12px 14px;margin:14px 0 0;min-height:3em;max-height:340px;overflow:auto;white-space:pre-wrap;word-break:break-all}
#kb-uit .fout{color:#ff8ae6}
#kb-uit .tijd{color:#9a9ab0}
"""
KLADBLOK_HTML = """  <div class="kaart">
    <h2>Kladblok (JavaScript)</h2>
    <p class="klein" style="margin-top:0">Schrijf code en klik op Voer uit. <code>console.log(...)</code> schrijft in het zwarte vak. Loopt de pagina vast? Herlaad ze.</p>
    <textarea id="kb-code" spellcheck="false" autocapitalize="off" aria-label="Code"></textarea>
    <div class="rij"><button class="primair" id="kb-voer" type="button">Voer uit</button><button id="kb-wis" type="button">Wis uitvoer</button><button id="kb-terug" type="button">Begincode terug</button></div>
    <pre id="kb-uit" aria-live="polite"></pre>
  </div>
"""
KLADBLOK_JS = """
(function () {
  const sleutel = "uhctf-kladblok-" + location.pathname;
  const veld = $("kb-code"), uit = $("kb-uit");
  let bewaard = null;
  try { bewaard = localStorage.getItem(sleutel); } catch (e) {}
  veld.value = bewaard || KLADBLOK;
  veld.addEventListener("input", () => { try { localStorage.setItem(sleutel, veld.value); } catch (e) {} });
  veld.addEventListener("keydown", e => {  // Tab springt niet uit het veld maar zet twee spaties
    if (e.key !== "Tab") return;
    e.preventDefault();
    const s = veld.selectionStart;
    veld.setRangeText("  ", s, veld.selectionEnd, "end");
  });
  function schrijfUit(tekst, klasse) {
    const regel = document.createElement("div");
    if (klasse) regel.className = klasse;
    regel.textContent = tekst;
    uit.appendChild(regel);
    uit.scrollTop = uit.scrollHeight;
  }
  const tekstVan = w => typeof w === "string" ? w : (() => { try { return JSON.stringify(w); } catch (e) { return String(w); } })();
  const nepConsole = { log: (...w) => schrijfUit(w.map(tekstVan).join(" ")) };
  nepConsole.info = nepConsole.warn = nepConsole.log;
  nepConsole.error = (...w) => schrijfUit(w.map(tekstVan).join(" "), "fout");
  $("kb-voer").addEventListener("click", () => {
    $("kb-voer").disabled = true;
    schrijfUit("> bezig ...", "tijd");
    setTimeout(() => {  // eerst tekenen, dan rekenen: anders zie je "bezig" niet
      const start = performance.now();
      try {
        const resultaat = new Function("console", veld.value)(nepConsole);
        if (resultaat !== undefined) schrijfUit(tekstVan(resultaat));
      } catch (e) {
        schrijfUit(e.name + ": " + e.message, "fout");
      }
      schrijfUit("> klaar in " + Math.round(performance.now() - start) + " ms", "tijd");
      $("kb-voer").disabled = false;
    }, 30);
  });
  $("kb-wis").addEventListener("click", () => { uit.textContent = ""; });
  $("kb-terug").addEventListener("click", () => {
    if (!confirm("Je eigen code wissen en de begincode terugzetten?")) return;
    veld.value = KLADBLOK;
    try { localStorage.removeItem(sleutel); } catch (e) {}
  });
})();
"""



def json_in_script(data) -> str:
    """JSON om in een <script> te zetten: een '</' in de tekst mag de scripttag niet afsluiten."""
    return json.dumps(data, ensure_ascii=False).replace("</", "<\\/")


def schrijf(uit: Path, titel: str, intro: str, body: str, script: Path, data: dict, hints: list[str], css: str = "",
            naam: str = BESTAND, kladblok: str | None = None) -> Path:
    """Schrijf uit/<naam> (standaard digitaal.html). 'body' en 'intro' zijn HTML, 'script' is het bestand met de logica van de uitdaging.
    Heeft een uitdaging varianten, dan heten de extra pagina's digitaal-2.html, digitaal-3.html, enz.
    'kladblok' (begincode) voegt onder de body een JavaScript-kladblok toe, voor uitdagingen waar je moet programmeren."""
    stijl = (SJABLONEN / "stijl.css").read_text() + css
    extra_js = ""
    if kladblok is not None:
        stijl += KLADBLOK_CSS
        body += "\n" + KLADBLOK_HTML
        extra_js = f"const KLADBLOK = {json_in_script(kladblok)};\n{KLADBLOK_JS}"
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
{extra_js}
</script>
</body>
</html>
"""
    pad = uit / naam
    pad.write_text(pagina)
    return pad


def inpakken(html: str, hints: list[str]) -> str:
    """Maak van een bestaande, zelfstandige pagina (zoals de beeldbewerker) een digitale pagina: markers voor de terug-link
    en de kluisknop, en de hints onderaan. De pagina houdt haar eigen stijl; de huisstijl komt er in de laptopmap bij."""
    if html.count("<main>") != 1 or html.count("</main>") != 1 or "</head>" not in html:
        raise ValueError("de pagina heeft een onverwachte opbouw: verwacht precies één <main> en een </head>")
    voet = (f"""  <div class="voet" id="hint-kaart">
    <div id="hints"></div>
    <button id="hint-knop" type="button">Hint</button>
    <!--KLUIS-->
  </div>
<script>
const HINTS = {json_in_script(hints)};
(function () {{
{GEMEENSCHAPPELIJK}
}})();
</script>
""")
    return (html.replace("</head>", "<!--STIJL-->\n</head>", 1).replace("<main>", "<main>\n  <!--NAV-->", 1)
            .replace("</main>", voet + "</main>", 1))
