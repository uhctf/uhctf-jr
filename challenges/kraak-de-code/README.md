<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Kraak de code

- Author: UHCTF

- Format: booth

- Age: 12–15

- Duration: 10–15 min

- Topic: Programmeren, recursie

- Materials: geprinte opgave (`deelnemer.pdf`), pen en papier of een computer

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>3455</code></li>
</ul></ul></details>

## Beschrijving

Geen mens zal dit ooit oplossen, je hebt zeker een computer nodig om deze code uit te voeren!

## Hints

1. De functie roept zichzelf op.
2. Begin klein: reken Code(2), Code(3), Code(4) uit.
3. Dit is de rij van Fibonacci. Plak daarna de twee uitkomsten (Code(9) en Code(10)) aan elkaar.

## Opzet

Het antwoord wordt berekend uit `functie` (`fibonacci`, `driehoek` of `verdubbel`), `a` en `b`. Er is dus geen vrij antwoord: pas die opties aan voor een ander event. Zet `hulp = true` voor een invultabel voor jongere deelnemers. Deelnemers kunnen de functie met de hand uitrekenen of in een programmeeromgeving naar keuze uitvoeren.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build kraak-de-code
```

Voor een event met andere opties:

```
./jr event add <event> kraak-de-code --set optie=waarde
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `functie` ("fibonacci"), `a` (9), `b` (10), `hulp` (false).

[SOLUTION.md](SOLUTION.md)
