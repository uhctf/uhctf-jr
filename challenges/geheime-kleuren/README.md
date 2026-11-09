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
<li>standaard: <code>ik eet graag pizza</code></li>
</ul></ul></details>

## Beschrijving

In deze wirwar van kleuren zit een geheime zin verstopt. Door elke gekleurde mica zie je een ander woord. Maar in welke volgorde horen ze? Volg de kleurcode.

## Hints

1. Kijk door elke mica. Zie je telkens iets anders?
2. Elke kleur mica toont één woord. Schrijf op welk woord bij welke kleur hoort.
3. Zet de woorden in de volgorde van de kleurcode.

## Opzet

De woorden liggen over elkaar in één afbeelding, elk in een andere inkt: het woord voor de rode filter in cyaan, voor de groene filter in magenta en voor de blauwe filter in geel. Elke inkt houdt precies één kleur licht tegen. Door een groene mica wordt het magenta woord dus donker, terwijl de andere woorden even licht lijken als het papier. De letters zijn opgebouwd uit driehoekjes (`vorm = "vol"` geeft volle letters) en liggen in een dichte wirwar van blokjes in blekere versies van dezelfde inkten. Met het blote oog verbergen de blokjes de woorden; door de filter worden ze lichtgrijs en blijft het woord donker.

**Kleurcode.** `volgorde` is de kleurcode en bepaalt welk woord bij welke kleur hoort: het eerste woord van het antwoord bij de eerste kleur, enzovoort. Meer woorden dan kleuren? Dan komen er vakken bij, en volgen de deelnemers de kleurcode in elk vak opnieuw. Met antwoord `ik eet graag pizza` en `volgorde = ["groen", "blauw"]` staan IK en EET in vak 1 en GRAAG en PIZZA in vak 2. De kleurcode staat niet op het blad (tenzij `kleurcode_op_blad = true`). Zo kun je ze laten vinden in een andere uitdaging: deel `kleurcode.pdf` uit als beloning, verwerk de kleuren in een raadsel, of gebruik een regenboog. Kies een zin waarin de volgorde ertoe doet, want zonder kleurcode kunnen deelnemers ook gokken.

**Afleiding (red herring).** Het woord in cyaan (rode filter) is ook zonder filter goed zichtbaar. Daarom staat er standaard een afleidingswoord in die kleur: `afleiding = "geen frietjes"` zet GEEN in vak 1 en FRIETJES in vak 2. Deelnemers zien dat meteen en denken dat ze klaar zijn; door de rode mica wordt het nog duidelijker, maar het hoort niet bij de kleurcode. Met `afleiding = ""` is er geen afleiding en kan `rood` weer in de `volgorde`. `afleiding_kleur` kiest de kleur (die mag niet in de volgorde staan).

**Leesbaarheid en verstoppen** zijn een evenwicht. `woord_sterkte` en `blokjes_sterkte` (0–100) bepalen hoe sterk de woorden en de blokjes gekleurd zijn: hoe groter het verschil, hoe beter leesbaar door de mica, maar ook hoe beter zichtbaar zonder mica. `snippers` is het aantal blokjes per kleur. `afleiding_sterkte` regelt hoe sterk de afleiding opvalt; te sterk maakt de plekken waar ze over de echte woorden ligt donker. Een andere `seed` geeft een andere wirwar.

**Mica's.** Per vak kunnen hoogstens drie woorden (rood, groen, blauw): licht en printerinkt hebben maar drie basiskleuren. Een gele, magenta, cyaan of oranje mica laat er twee door en toont dus twee woorden door elkaar. Ook een groene of blauwe mica die een beetje van de andere kleur doorlaat (zoals turquoise of lichtblauw) maakt het woord minder donker. Print `deelnemer.pdf` **in kleur** en maak een testafdruk met de mica's die je gaat gebruiken. `begeleider.pdf` toont wat een ideale filter laat zien; een echte mica is minder scherp.

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

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `volgorde` (["groen", "blauw"]), `kleurcode_op_blad` (false), `afleiding` ("geen frietjes"), `afleiding_kleur` ("rood"), `afleiding_sterkte` (90), `vorm` ("driehoekjes"), `snippers` (2500), `woord_sterkte` (80), `blokjes_sterkte` (70), `met_beeldbewerker` (false).

Extra vereiste: installeer met `./jr install geheime-kleuren`.

[SOLUTION.md](SOLUTION.md)
