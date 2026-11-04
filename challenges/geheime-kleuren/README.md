<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Geheime kleuren

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Kleurfilters, licht en kleur, verborgen informatie

- Materials: kleurenafdruk van `deelnemer.pdf`, gekleurde mica's of folie (rood en blauw/cyaan; een rood-cyaan 3D-brilletje werkt ook)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>kijk-beter</code></li>
</ul></ul></details>

## Beschrijving

Op dit blad staan geheime woorden, maar ze zijn verstopt onder een wirwar van kleuren. Met gekleurde mica's kun je dingen zien die je ogen alleen niet zien.

## Hints

1. Kijk door elke mica naar elk vak. Wat verdwijnt er?
2. Een rode mica laat rode krabbels verdwijnen. Welke kleur heeft de wirwar in elk vak?
3. Gebruik voor elk vak de mica met dezelfde kleur als de wirwar, en zet de woorden in volgorde.

## Opzet

Elk vak bevat een woord in een lichte kleur, verstopt onder camouflage (krabbels en nep-letters) in de kleur van een filter. Door een filter van die kleur lijkt de camouflage even licht als het papier en wordt het woord donker. Door een andere filter blijft het een wirwar. Het antwoord wordt verdeeld over de vakken (op `-` of spatie, anders in gelijke stukken).

Print `deelnemer.pdf` **in kleur**. Printers en mica's verschillen: maak een testafdruk en kijk door de mica's of de woorden goed leesbaar zijn en zonder mica goed verstopt. `begeleider.pdf` toont hoe elk vak eruitziet door de juiste filter (dat is een ideale filter; een echte mica is iets minder scherp). Een rood-cyaan 3D-brilletje werkt voor `rood` en `blauw`. Met een andere `seed` krijg je andere camouflage.

`kleuren.png` bevat alle vakken, om groter te printen of op een scherm te tonen. Met `met_beeldbewerker = true` komt de [beeldbewerker](../_gedeeld/beeldbewerker/) mee met die afbeelding ingebouwd: één kleurkanaal tonen werkt als een perfecte filter. Handig als er geen mica's zijn, of als uitbreiding voor oudere deelnemers.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build geheime-kleuren
```

Voor een event met een eigen antwoord:

```
./jr event add <event> geheime-kleuren --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `filters` (["rood", "blauw"]), `met_beeldbewerker` (false).

Extra vereiste: installeer met `./jr install geheime-kleuren`.

[SOLUTION.md](SOLUTION.md)
