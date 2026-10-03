<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Doolhof

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Puzzelen, geduld

- Materials: geprint doolhof (`deelnemer.pdf`), potlood

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>securityrocks</code></li>
</ul></ul></details>

## Beschrijving

Vind je weg door het doolhof, de reis brengt de beloning.

## Hints

1. Het doolhof staat vol letters.
2. Volg de route van Start naar End.
3. Schrijf de letters op die je tegenkomt, in de juiste volgorde.

## Opzet

Print `deelnemer.pdf` (1 per deelnemer of team) en geef potloden mee. Dezelfde `seed` geeft altijd hetzelfde doolhof; verander hem voor een nieuw doolhof. `begeleider.pdf` bevat een afbeelding van de juiste route.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build doolhof
```

Voor een event met een eigen antwoord:

```
./jr event add <event> doolhof --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (2025), `breedte` (14), `hoogte` (18).

[SOLUTION.md](SOLUTION.md)
