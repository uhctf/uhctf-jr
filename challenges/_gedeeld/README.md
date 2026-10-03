<!-- Dit bestand wordt gegenereerd uit resource.toml. Pas resource.toml aan en draai ./jr readme. -->

# Gedeeld materiaal

Hulpmiddelen die door meerdere uitdagingen gebruikt worden. Uitdagingen leveren ze mee in hun uitvoer, in een map met de naam van het hulpmiddel (bv. `decoder/`). Dit bestand wordt gegenereerd uit de `resource.toml` van elk hulpmiddel.

## Beeldbewerker

- `beeldbewerker/` (gegenereerd)

Webpagina om een afbeelding te bekijken en te bewerken: helderheid, contrast, kleurkanalen, inverteren en meer. Handig voor verborgen informatie in afbeeldingen. Werkt offline in de browser, in het Nederlands en Engels. Een standaardafbeelding kan ingebouwd worden, zodat die meteen geladen is.

Gebruik: Bouw met `./jr shared build beeldbewerker --set afbeelding=pad/naar/afbeelding.png` (opties `afbeelding` en `taal`). De afbeelding zit dan in `beeldbewerker/index.html` zelf, zodat de pagina ook vanaf schijf zonder internet werkt. Andere afbeeldingen opent een deelnemer met 'Open afbeelding' of door ze op de pagina te slepen; met een webserver kan ook `index.html#afbeelding=qr.png`. De knop 'Standaardafbeelding' laadt de ingebouwde afbeelding opnieuw.

## Decoder

- `decoder/` (statisch)

Webpagina om berichten te coderen en decoderen: Base64, hexadecimaal, binair, morse, ROT-N en XOR, met meerdere stappen na elkaar. Werkt offline in de browser, in het Nederlands en Engels.

Gebruik: Open `decoder/index.html` in een browser. De opstelling (invoer en stappen) staat in de URL na `#`, zodat een begeleider een kant-en-klare link kan delen. Voorbeeld: `index.html#t=nl&i=PXIXA&s=rot:3`.

## Spiekbrief

- `spiekbrief/` (gegenereerd)

Afdrukbare spiekbrief (pdf) over binair, hexadecimaal, Base64, ROT-N, XOR en morse, met voorbeelden die de generator zelf uitrekent.

Gebruik: Bouw met `./jr shared build spiekbrief` (optie `--set taal=en`). Uitdagingen die codering gebruiken, leveren de spiekbrief mee in hun uitvoer.
