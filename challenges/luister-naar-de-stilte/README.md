<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Luister naar de stilte

- Author: UHCTF

- Format: booth

- Age: 15–18

- Duration: 15–25 min

- Topic: Geluid ontleden, spectrogram, morse, verborgen informatie

- Materials: laptop met de WAV-decoder (de digitale pagina), de morsetabel (spiekbrief) en de Decoder; koptelefoon is niet nodig

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>radiostilte</code></li>
</ul></ul></details>

## Beschrijving

Een onderzoeker nam in een verlaten radiohut een halve minuut stilte op. Toch beweert zijn collega dat er een boodschap in zit. Je hoort bijna niets, maar een geluidsbestand is meer dan wat je hoort.

## Hints

1. Je hoort bijna niets. Maar een geluid kun je ook bekijken: kijk naar de golfvorm en naar het spectrogram.
2. Zet 'Versterken' hoger en pas helderheid en contrast van het spectrogram aan. De x-as is tijd, de y-as is frequentie. Zoek een rij streepjes en puntjes die steeds op dezelfde hoogte staat.
3. Zie je meer dan een rij? Lees ze allemaal af. Niet elk bericht dat je vindt, is het antwoord.
4. Zoom in en lees de korte en lange streepjes af. Een streep is drie keer zo lang als een punt.
5. Schrijf de punten en strepen op en zet ze om met de morsetabel van de spiekbrief, of met de Decoder (stap Morse naar tekst).

## Opzet

`stilte.wav` is een gewoon WAV-bestand (44,1 kHz, mono, 16 bit) dat de generator met enkel de standaardbibliotheek van Python maakt. In het standaardniveau (`moeilijk`) zit de morse in een toon van ongeveer 17 kHz met een amplitude van 0,55% van de volle schaal, onder witte ruis en een zacht netbrom. Een laptopluidspreker geeft die toon nauwelijks weer en veel mensen horen hem niet. In het spectrogram is hij een rij streepjes en puntjes (met Helderheid en Contrast goed te lezen). Daarnaast speelt een duidelijker morsesignaal op 1300 Hz dat 'lokvogel' seint: wie enkel op de golfvorm of de oren afgaat, vindt dat eerst en typt een fout antwoord. Het echte bericht staat twee keer na elkaar.

De digitale versie is de **WAV-decoder** met het geluid ingebouwd: de kop van het bestand, de golfvorm met versterking en een spectrogram. De morse wordt dus enkel zichtbaar gemaakt, niet gedecodeerd. De deelnemers moeten zelf (1) inzien dat er iets in zit, (2) de rij vinden in het spectrogram, (3) de puntjes en streepjes aflezen en (4) ze omzetten naar tekst met de morsetabel of de Decoder.

Niveaus: `makkelijk` (een hoorbare piep van 700 Hz, ook te volgen op het gehoor), `middel` (een zachte toon rond 1200 Hz in ruis) en `moeilijk` (standaard). Met `seed` verandert de exacte frequentie.

Tips voor het event:

- Het werkt volledig met de ogen. Laat dus niet zes teams tegelijk geluid afspelen: koptelefoons zijn niet nodig.
- Test de pagina op elke laptop (Chrome of Edge): de spectrogramberekening duurt even bij het openen.
- Bespreking: onhoorbaar is niet afwezig, net zoals onzichtbaar niet verborgen is (zie Robot-QR). Audio-steganografie: informatie in geluid verstoppen, bijvoorbeeld in het spectrogram.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build luister-naar-de-stilte
```

Voor een event met een eigen antwoord:

```
./jr event add <event> luister-naar-de-stilte --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `niveau` ("moeilijk"), `herhalingen` (2), `digitaal` (true).

[SOLUTION.md](SOLUTION.md)
