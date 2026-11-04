<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Kies je kant

- Author: UHCTF

- Format: booth

- Age: 12–18

- Duration: 3–5 min

- Topic: Kleuren en kleurcodes (hexadecimaal, RGB), de groep in twee ploegen verdelen

- Materials: uitgeknipte kaartjes (`deelnemer.pdf`), zwart-wit printen volstaat

- Flag Format: geen vlag; de opdracht zelf is de actie

## Beschrijving

Op je kaartje staat een kleurcode. Lees ze af: welke kleur is het, Cyaan of Magenta? Zoek dan de anderen met dezelfde kleur, zonder die hardop te zeggen. Samen vormen jullie een ploeg.

## Hints

1. De grijze achtergrond zegt niets. Kijk naar de code.
2. De code bestaat uit drie paren (rood, groen, blauw). Een paar dat met 0 tot 7 begint, is laag; één paar is laag.
3. Rood laag is Cyaan, groen laag is Magenta.

## Opzet

Print `deelnemer.pdf` (zwart-wit volstaat) en knip de kaartjes uit. Elk kaartje heeft enkel een kleurcode op een grijze, gearceerde achtergrond: de achtergrond zegt niets over de kleur, ze moeten de code lezen. Bovenaan de eerste pagina staat een korte uitleg voor op het bord of de beamer (niet op de kaartjes). Deel de kaartjes één voor één uit, in de volgorde van de stapel: ze staan per twee in willekeurige volgorde (één Cyaan, één Magenta), dus de ploegen zijn even groot. Bij een oneven aantal deelnemers is één ploeg één persoon groter.

Laat iedereen zijn kleur uit de code afleiden en de anderen met dezelfde kleur vinden. Ze mogen elkaars kaartjes bekijken maar de kleur niet hardop zeggen. Dat kost twee à vijf minuten. Controleer daarna met `begeleider.pdf` of iedereen in de juiste ploeg staat.

De twee ploegen, Cyaan en Magenta, strijden tegen elkaar. `begeleider.pdf` heeft achteraan een scoreblad om per team de open sloten en het uur van de open kluis te noteren. Binnen elke ploeg vormen de deelnemers teams van 2 à 3. Er is geen antwoord en geen slot in de kluis.

Het is een eerste kennismaking met hexadecimale kleurcodes, die ze later bij Robot-QR terugzien (kleurkanalen).

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build kies-je-kant
```

Voor een event met andere opties:

```
./jr event add <event> kies-je-kant --set optie=waarde
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `aantal` (16).

[SOLUTION.md](SOLUTION.md)
