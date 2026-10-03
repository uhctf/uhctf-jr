<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Woordzoeker

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Puzzelen, observeren

- Materials: geprinte woordzoeker (`deelnemer.pdf`), potlood

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>passwords</code></li>
</ul></ul></details>

## Beschrijving

Soms zit de meeste waarde verborgen in het volle zicht.

## Hints

1. Zoek eerst alle woorden uit de lijst en kruis ze af.
2. Niet elke letter hoort bij een woord.
3. Lees de overgebleven letters in leesrichting (links naar rechts, boven naar onder).

## Opzet

Print `deelnemer.pdf` en geef potloden mee. Met `moeilijk = true` mogen woorden ook achterstevoren en schuin omhoog staan. `grootte` en `woorden` bepalen het raster; de overgebleven letters spellen altijd het antwoord.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build woordzoeker
```

Voor een event met een eigen antwoord:

```
./jr event add <event> woordzoeker --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (2025), `grootte` (7), `moeilijk` (false), `woorden` (["encrypt", "flag", "puzzle", "byte", "code", "key", "shift", "file", "web", "hash", "bit", "login"]).

[SOLUTION.md](SOLUTION.md)
