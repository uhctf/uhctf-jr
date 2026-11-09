<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Geheime kleuren

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Kleurfilters, licht en kleur, verborgen informatie

- Materials: kleurenafdruk van `deelnemer.pdf`, rode, groene en blauwe mica's of folie, de kleurcode (`kleurcode.pdf` of uit een andere uitdaging)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>ik eet pizza</code></li>
</ul></ul></details>

## Beschrijving

In deze wirwar van kleuren zit een geheime zin verstopt. Door elke gekleurde mica zie je een ander woord. Maar in welke volgorde horen ze? Volg de kleurcode.

## Hints

1. Kijk door elke mica. Zie je telkens iets anders?
2. Elke kleur mica toont één woord. Schrijf op welk woord bij welke kleur hoort.
3. Zet de woorden in de volgorde van de kleurcode.

## Opzet

De woorden liggen over elkaar in één afbeelding, elk in een andere inkt: het woord voor de rode filter in cyaan, voor de groene filter in magenta en voor de blauwe filter in geel. Elke inkt houdt precies één kleur licht tegen. Door een rode mica wordt het cyaan woord dus donker, terwijl het magenta en het gele woord even licht lijken als het papier. Zo zijn de woorden elkaars camouflage, met extra snippers in dezelfde inkten.

`volgorde` is de kleurcode en bepaalt welk woord bij welke kleur hoort: het eerste woord van het antwoord bij de eerste kleur, enzovoort. Met `volgorde = ["blauw", "rood", "groen"]` en antwoord `ik eet pizza` staat "IK" dus in het geel.

Meer woorden dan kleuren? Dan komen er vakken bij, en volgen de deelnemers de kleurcode in elk vak opnieuw. Met antwoord `ik eet graag pizza scampi` en de standaardkleurcode staan IK, EET en GRAAG in vak 1 en PIZZA en SCAMPI in vak 2. Een vak met minder woorden krijgt toch snippers in alle inkten, zodat het even goed verstopt blijft.

Meer dan drie kleuren per vak kan niet: licht en printerinkt hebben maar drie basiskleuren. Een gele, magenta, cyaan of oranje mica laat er twee door en toont dus twee woorden door elkaar. Gebruik een rode, een groene (turquoise werkt ook) en een blauwe mica, en test eventueel welke andere mica's ook werken. De kleurcode staat niet op het blad (tenzij `kleurcode_op_blad = true`). Zo kun je ze laten vinden in een andere uitdaging: deel `kleurcode.pdf` uit als beloning, verwerk de kleuren in een raadsel, of gebruik een regenboog (rood, groen, blauw van boven naar onder) bij de standaardvolgorde. Kies een zin waarin de volgorde ertoe doet, want zonder kleurcode kunnen deelnemers ook gokken.

Print `deelnemer.pdf` **in kleur**. Je hebt drie mica's nodig: rood, groen en blauw. Een rood-cyaan 3D-brilletje werkt hier niet, want een cyaan filter laat zowel groen als blauw door. Printers en mica's verschillen: maak een testafdruk en kijk of elk woord door zijn mica goed leesbaar is. `begeleider.pdf` toont wat een ideale filter laat zien; een echte mica is iets minder scherp. Zijn de woorden met het blote oog nog te goed leesbaar, verhoog dan `snippers` of probeer een andere `seed`.

`kleuren.png` is de afbeelding zelf, om groter te printen of op een scherm te tonen. Met `met_beeldbewerker = true` komt de [beeldbewerker](../_gedeeld/beeldbewerker/) mee met die afbeelding ingebouwd: één kleurkanaal tonen werkt als een perfecte filter.

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

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `volgorde` (["rood", "groen", "blauw"]), `kleurcode_op_blad` (false), `snippers` (500), `met_beeldbewerker` (false).

Extra vereiste: installeer met `./jr install geheime-kleuren`.

[SOLUTION.md](SOLUTION.md)
