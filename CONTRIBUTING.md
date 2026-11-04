# Bijdragen / Contributing

## Aan de slag

Je hebt Python 3.11 of nieuwer nodig.

```
./jr setup          # maakt .venv en installeert requirements.txt
./jr list           # toont alle uitdagingen
```

`./jr` start zelf in de virtuele omgeving, je hoeft die niet te activeren.

## Soorten uitdagingen

- **Gegenereerd** (`type = "generated"`): een `generate.py` maakt de pdf's en andere bestanden. Er is altijd een standaardantwoord. Events kunnen het antwoord en de opties overschrijven.
- **Statisch** (`type = "static"`): vast materiaal in `src/`. Een statische uitdaging kan niet event-specifiek gebouwd worden. De tooling weigert een antwoord of opties daarvoor.

Gebruik gegenereerd waar het kan: dan kan elk event een eigen antwoord kiezen, ook al zijn de oplossingen publiek.

## Nieuwe uitdaging

```
./jr new mijn-uitdaging            # gegenereerd
./jr new mijn-uitdaging --statisch # statisch
```

Dit maakt `challenges/mijn-uitdaging/` met:

- `challenge.toml`: **alle** gegevens van de uitdaging (zie hieronder)
- `README.md`: wordt **gegenereerd** uit `challenge.toml`, niet met de hand aanpassen
- `SOLUTION.md`: de oplossing, met de hand geschreven (aparte file, zodat testers niets per ongeluk zien)
- `generate.py` (gegenereerd) of `src/` (statisch)

### challenge.toml

```toml
type = "generated"          # of "static"
antwoord = "salad"          # standaardantwoord (weglaten als het berekend wordt)

[opties]                    # opties voor generate.py, door events te overschrijven
taal = "nl"

[meta]
auteur = "UHCTF"
formaat = "booth"
leeftijd = "8–12"
duur = "5–10 min"
vlag_formaat = "antwoord"   # of "uhctf" voor uhctf{...}, of "geen" als de actie zelf de opdracht is

[nl]                        # hoofdtaal; een [en]-tabel levert README.en.md op
naam = "Romeinse geheimen"
onderwerp = "Caesarcijfer"
materiaal = "geprint bericht, laptop"
beschrijving = '''...'''
hints = ["...", "...", "..."]
opzet = '''...'''            # extra uitleg; bouwinstructies en opties komen er automatisch bij
```

Statische uitdagingen hebben geen `antwoord` maar `vlaggen = [["label", "waarde"], ...]`.

Na elke wijziging aan `challenge.toml`:

```
./jr readme             # schrijft de README's en het overzicht in challenges/README.md
./jr readme --check     # faalt als een README niet meer klopt (ook onderdeel van ./jr check --alles)
```

### generate.py

```python
def generate(params, uit) -> str   # schrijf bestanden in 'uit', geef het antwoord terug
def check(params) -> None          # optionele zelftest, gooit een fout als iets niet klopt
```

`params` bevat `antwoord` en alles uit `[opties]` van `challenge.toml`, met eventuele overrides. Gebruik `from jr.pdf import Pdf, begeleider` voor pdf's, `from jr import codecs` voor coderingen en `from jr.shared import gebruik` om gedeeld materiaal mee te leveren (`gebruik(uit, taal, "decoder", "spiekbrief")`, zie hieronder). Lever minstens `deelnemer.pdf` en `begeleider.pdf` (antwoord, oplossing, hints).

Heeft een uitdaging een extra bibliotheek nodig, maak dan een `requirements.txt` in haar map met enkel die vereisten (er is er geen tot dat nodig is). Installeren kan met `./jr install mijn-uitdaging`.

Is het antwoord berekend (zoals bij `kraak-de-code`), laat dan `antwoord` weg uit `challenge.toml`.

### Testen

```
./jr check mijn-uitdaging      # bouwt met standaardwaarden en voert check() uit
./jr check --alles
./jr build mijn-uitdaging --antwoord woord --set seed=3 --uit /tmp/proef
```

## Gedeeld materiaal

Hulpmiddelen die meerdere uitdagingen gebruiken staan in `challenges/_gedeeld/<naam>/`, met een `resource.toml` (`type = "static"` of `"generated"`, plus `[nl]`/`[en]`-tekst). Een gegenereerde bron heeft een `generate.py` met dezelfde contract als een uitdaging. Uitdagingen leveren ze mee in hun uitvoer, in een map met dezelfde naam (`<uitvoer>/decoder/index.html`).

```
./jr shared list
./jr shared build spiekbrief --set taal=en
./jr shared build beeldbewerker --set afbeelding=foto.png   # met ingebouwde standaardafbeelding
./jr shared check spiekbrief
```

Een generator geeft opties door aan een gedeelde bron met `gebruik(uit, taal, "beeldbewerker", opties={"beeldbewerker": {"afbeelding": str(pad)}})`.

De README van `_gedeeld` wordt net als die van uitdagingen gegenereerd (`./jr readme`).

## Events

```
./jr event new mijn-event
./jr event add mijn-event doolhof --antwoord kangoeroe --set breedte=10
./jr event add mijn-event webvlaggen         # statisch: zonder overrides
./jr event show mijn-event
./jr event install mijn-event                # vereisten van alle uitdagingen in het event
./jr event build mijn-event                  # schrijft events/mijn-event/out/
```

De keuze staat in `events/<event>/event.toml`. `out/` bevat per uitdaging het materiaal en `ANTWOORDEN.pdf` met alle antwoorden (voor begeleiders). `out/` wordt niet in git bewaard: bouw het vlak voor het event, en deel de pdf's.

### Laptopmap

Staat er een tabel `[laptop]` in `events/<event>/event.toml`, dan maakt `./jr event build` ook `out/laptop/`: een map die je naar een laptop kopieert en zonder internet of server opent via `index.html`. Ze bevat een startpagina, de decoder, de kluis en de digitale versies van de uitdagingen.

```toml
[laptop]                     # gereserveerde tabel: dit is geen uitdaging
titel = "Naam op de startpagina"
nodig = 3                    # aantal sloten voor de kluis opengaat; "alle" = elk slot van het event
intro = "Welkom! ... {nodig} sloten"  # optioneel: tekst bovenaan de startpagina; {nodig} wordt het aantal sloten
```

De kluis kent de antwoorden van alle uitdagingen in het event, als hash. Bij meerdere antwoorden (varianten) geeft `generate()` meerdere regels terug in de vorm `label: antwoord`; het deel na de eerste `: ` telt als antwoord. Hoofdletters, spaties en leestekens tellen niet mee. Een statische uitdaging met meerdere `vlaggen` krijgt een slot per vlag.

Een statische uitdaging die zelf een site is (zoals `webvlaggen`), komt in de laptopmap met `laptop_map = "src"` in haar `challenge.toml`: die map wordt `laptop/<uitdaging>/`, zonder aanpassingen aan de pagina. De site moet dan vanaf schijf werken (geen `fetch`, wel `<script src>`). Dat kan ook voor een gegenereerde uitdaging (zoals `hack-het-portaal`): `generate.py` schrijft de site in de map uit `laptop_map` (bv. `site/`) in de uitvoer. Staat er `<!--TERUG-->` in een pagina, dan komt daar in de laptopmap een link naar de startpagina; elders blijft het commentaar. Een uitdaging die zelf iets onthoudt in `localStorage` gebruikt sleutels met het voorvoegsel `opdracht-`: "Nieuw team" in de kluis wist die (en de kladblokken).

### Digitale versie van een uitdaging

Een gegenereerde uitdaging kan er ook een digitale versie bij maken: een zelfstandige webpagina die offline werkt. In `challenge.toml` staat daarvoor de optie `digitaal = false` onder `[opties]`. Een event zet hem aan met `digitaal = true` in `event.toml` (of `./jr event add <event> <uitdaging> --set digitaal=ja`).

In `generate()`:

```python
from jr.digitaal import schrijf

if params.get("digitaal"):
    schrijf(uit, "Titel", "uitleg", body_html, Path(__file__).parent / "digitaal.js", data, hints)
```

`schrijf` maakt `uit/digitaal.html` met de puzzel als `DATA` (JSON), `HINTS` en het script uit `digitaal.js`, in de stijl van de laptopmap. Het script mag `$(id)` gebruiken. Heeft de uitdaging varianten, geef dan `naam="digitaal-2.html"` mee voor de volgende. In de laptopmap komen die als `<uitdaging>/index.html` en `<uitdaging>/variant-2.html`, met een terug-link en een knop naar de kluis. Verwijs naar de decoder als `decoder/index.html`: dat pad wordt in de laptopmap aangepast. Moeten deelnemers programmeren, geef dan `kladblok="begincode"` mee aan `schrijf`: onder de puzzel komt een JavaScript-kladblok met een uitvoervak voor `console.log` (zie `kraak-de-code`). Is de digitale versie een bestaande, zelfstandige pagina (zoals de beeldbewerker bij `robot-qr`), gebruik dan `inpakken(html, hints)` uit `jr.digitaal`: dat voegt de terug-link, de hints en de knop naar de kluis toe. Een digitale versie is een hulpmiddel, zoals de decoder: ze helpt met de puzzel maar controleert niet of de oplossing juist is en zegt niet wanneer je klaar bent. De kinderen typen het antwoord zelf in de kluis. Een uitzondering is een mechanisme dat bij het spel hoort, zoals de feedback per vak bij de mastermind (de rol van de begeleider op papier). De pagina's hebben de huisstijl van UHCTF: licht, scherpe hoeken (geen afgeronde hoeken, ook niet bij knoppen of badges; alleen een figuur die echt rond is, zoals het caesarwiel, blijft rond), donkergrijs met magenta en cyaan als accent. `tools/jr/laptop_sjablonen/stijl.css` zit er al in; gebruik de variabelen daarvan (`var(--cyaan)`, `var(--lijn)`, ...) in de eigen `css` van een uitdaging. Houd de tekst op de pagina kort (een zin uitleg, geen paragrafen): kinderen worden overdonderd door veel tekst. Houd de puzzel gelijk aan de papieren versie, zodat het antwoord hetzelfde blijft, en zet geen antwoord of oplossing in `DATA` als dat vermijdbaar is.

## Regels

- Nederlands eerst, Engels optioneel (`.en.md`; generatoren hebben de optie `taal`).
- Geen persoonsgegevens, geen echte externe doelwitten.
- Voeg enkel derde-partijmateriaal toe met een compatibele licentie, en vermeld de bron.
- Met je bijdrage ga je akkoord met de licenties: CC BY-NC-SA 4.0 voor inhoud, MIT voor code.
