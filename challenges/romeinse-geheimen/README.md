<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Romeinse geheimen

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Caesarcijfer (ROT-N)

- Materials: geprint bericht (`deelnemer.pdf`), laptop of tablet met de [decoder](../_gedeeld/decoder/), [spiekbrief](../_gedeeld/spiekbrief/) (optioneel)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>salad</code></li>
</ul></ul></details>

## Beschrijving

Een archeoloog vond een bericht dat lijkt te zijn gecodeerd door een keizer.

Het bericht: `PXIXA`

## Hints

1. Welke keizer gebruikte een geheimschrift waarbij je letters verschuift?
2. Het is een Caesarcijfer: elke letter is een vast aantal plaatsen verschoven.
3. Probeer in de [decoder](../_gedeeld/decoder/) de stap ROT-N met kleine getallen.

## Opzet

Deelnemers gebruiken de meegeleverde [decoder](../_gedeeld/decoder/) (lokaal in de browser, geen internet nodig) of de strook op `deelnemer.pdf`. De [spiekbrief](../_gedeeld/spiekbrief/) kan er bij geprint worden. `verschuiving` is het aantal letters. Het bericht staat ook in `bericht.txt`.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build romeinse-geheimen
```

Voor een event met een eigen antwoord:

```
./jr event add <event> romeinse-geheimen --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `verschuiving` (3).

[SOLUTION.md](SOLUTION.md)
