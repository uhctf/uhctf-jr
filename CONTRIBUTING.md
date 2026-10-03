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
- `requirements.txt`: extra vereisten enkel voor deze uitdaging
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

Heeft een uitdaging een extra bibliotheek nodig, zet die in haar eigen `requirements.txt`. Installeren kan met `./jr install mijn-uitdaging`.

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

De keuze staat in `events/<event>/uitdagingen.toml`. `out/` bevat per uitdaging het materiaal en `ANTWOORDEN.pdf` met alle antwoorden (voor begeleiders). `out/` wordt niet in git bewaard: bouw het vlak voor het event, en deel de pdf's.

## Regels

- Nederlands eerst, Engels optioneel (`.en.md`; generatoren hebben de optie `taal`).
- Geen persoonsgegevens, geen echte externe doelwitten.
- Voeg enkel derde-partijmateriaal toe met een compatibele licentie, en vermeld de bron.
- Met je bijdrage ga je akkoord met de licenties: CC BY-NC-SA 4.0 voor inhoud, MIT voor code.
