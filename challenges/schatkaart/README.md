<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Schatkaart

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 10 min

- Topic: Raadsels oplossen, coördinaten

- Materials: geprinte kaart met raadsels (`deelnemer.pdf`), potlood

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>sleutel</code></li>
</ul></ul></details>

## Beschrijving

Piraat Rik heeft zijn schat verstopt, maar de kaart staat vol stippen. Welke stippen zijn de juiste? Alleen de raadsels weten het.

## Hints

1. Los eerst alle raadsels op: schrijf per raadsel een letter en een getal op.
2. Een plaats heet bv. C4: kolom C, rij 4. Zoek de stip daar.
3. Veel stippen horen bij geen enkel raadsel. Negeer die.

## Opzet

Print `deelnemer.pdf` per kind of team en geef potloden mee. Op het blad staat een kaart met een raster (kolommen A tot J, rijen 1 tot 10) en veel stippen, elk met een letter. Elk raadsel bestaat uit twee delen: een kolomraadsel (het antwoord is een letter) en een rijraadsel (het antwoord is een getal). Samen wijzen ze één stip aan. De letters bij die stippen, in volgorde van de raadsels, spellen het antwoord. De meeste stippen zijn afleiders: zonder de raadsels weet je niet welke de juiste zijn.

Met `antwoord` bepaal je het wachtwoord (3 tot 12 letters, één raadsel per letter) en met `punten` hoeveel stippen er in totaal staan. `begeleider.pdf` bevat de oplossing per raadsel en een kaart met de juiste stippen omcirkeld en met een lijn verbonden. De raadsels zijn zelf geschreven voor 10 à 11 jaar; ze komen uit vaste lijsten in `generate.py`. Voeg daar eigen raadsels aan toe voor een andere doelgroep. Met `digitaal = true` komt er ook een klikbare kaart bij voor op een laptop (`digitaal.html`): de kinderen kiezen een raadsel en klikken op de stip die erbij hoort.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build schatkaart
```

Voor een event met een eigen antwoord:

```
./jr event add <event> schatkaart --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (2025), `punten` (45), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
