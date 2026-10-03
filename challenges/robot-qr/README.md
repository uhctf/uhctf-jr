<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Robot-QR

- Author: UHCTF

- Format: booth

- Age: 12–15

- Duration: 10–15 min

- Topic: Afbeeldingen bewerken, QR-codes, verborgen informatie

- Materials: laptop of tablet met de [beeldbewerker](../_gedeeld/beeldbewerker/) (met de QR-code ingebouwd); een telefoon om de QR-code te scannen; optioneel een 3D-geprinte robot

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>night-vision</code></li>
</ul></ul></details>

## Beschrijving

Afbeeldingen kunnen meer bevatten dan op het eerste zicht lijkt.

Op de foto staat een zwarte 3D-geprinte robot met een QR-code op zijn borst. De code is donkerblauw op zwart en dus bijna onzichtbaar. Met de afbeeldingsbewerker kun je de foto aanpassen.

## Hints

1. Je ogen zien de QR-code nauwelijks. Een beeld kan aangepast worden.
2. Speel met belichting en de kleurkanalen in de bewerker.
3. Een QR-code is meestal zwart op wit. Probeer ook Inverteren, en scan dan met een telefoon.

## Opzet

De QR-code wordt gegenereerd uit het antwoord, in donkerblauw op zwart. Deelnemers openen `beeldbewerker/index.html` lokaal in de browser (geen internet nodig). De QR-code is als standaardafbeelding ingebouwd, dus de afbeelding staat meteen klaar. `qr.png` is de afbeelding zelf, handig om te printen. Optie `schaal` stelt de grootte van de pixels in. Voor extra beleving kan de QR-code in donkerblauw op zwart filament op een 3D-geprinte robot staan. Een event kan een foto van die robot gebruiken: zet `afbeelding = "robot.jpg"` in `uitdagingen.toml` (pad vanaf de eventmap, bv. `./jr event add <event> robot-qr --set afbeelding=robot.jpg`). De foto wordt dan in de beeldbewerker ingebouwd in plaats van de gegenereerde code, en het antwoord moet overeenkomen met de QR-code op de foto.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build robot-qr
```

Voor een event met een eigen antwoord:

```
./jr event add <event> robot-qr --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `schaal` (12), `kleur` ("#000028"), `afbeelding` ("").

Extra vereiste: installeer met `./jr install robot-qr`.

[SOLUTION.md](SOLUTION.md)
