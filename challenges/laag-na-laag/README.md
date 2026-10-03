<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Laag na laag

- Author: UHCTF

- Format: booth

- Age: 12–15

- Duration: 10–15 min

- Topic: Base64, hexadecimaal, binair

- Materials: geprint bericht (`deelnemer.pdf`, ook als `bericht.txt`), laptop of tablet met de [decoder](../_gedeeld/decoder/), [spiekbrief](../_gedeeld/spiekbrief/)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>layers-of-security</code></li>
</ul></ul></details>

## Beschrijving

Dit bericht lijkt moeilijker te ontcijferen, alsof iemand het meerdere lagen diep heeft verborgen.

```
MzAzMTMxMzAzMTMxMzAzMDIwMzAzMTMxMzAzMDMwMzAzMTIwMzAzMTMxMzEzMTMwMzAzMTIwMzAzMTMxMzAzMDMxMzAzMTIwMzAzMTMxMzEzMDMwMzEzMDIwMzAzMTMxMzEzMDMwMzEzMTIwMzAzMDMxMzAzMTMxMzAzMTIwMzAzMTMxMzAzMTMxMzEzMTIwMzAzMTMxMzAzMDMxMzEzMDIwMzAzMDMxMzAzMTMxMzAzMTIwMzAzMTMxMzEzMDMwMzEzMTIwMzAzMTMxMzAzMDMxMzAzMTIwMzAzMTMxMzAzMDMwMzEzMTIwMzAzMTMxMzEzMDMxMzAzMTIwMzAzMTMxMzEzMDMwMzEzMDIwMzAzMTMxMzAzMTMwMzAzMTIwMzAzMTMxMzEzMDMxMzAzMDIwMzAzMTMxMzEzMTMwMzAzMQ==
```

## Hints

1. Het einde van het bericht eindigt op `==`. Dat is een kenmerk van Base64.
2. Na Base64 krijg je cijfers en letters (hexadecimaal). Decodeer die ook.
3. De derde laag is binair (nullen en enen). Gebruik in de decoder drie stappen na elkaar.

## Opzet

`lagen` is de volgorde waarin het antwoord wordt ingepakt, uit `binair`, `hex`, `base64`, `rot13` en `morse`. Deelnemers pakken in omgekeerde volgorde uit met de meegeleverde [decoder](../_gedeeld/decoder/), waar meerdere stappen na elkaar kunnen. Het bericht staat ook in `bericht.txt` om te kopiëren. Zie ook [Romeinse geheimen](../romeinse-geheimen/README.md).

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build laag-na-laag
```

Voor een event met een eigen antwoord:

```
./jr event add <event> laag-na-laag --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `lagen` (["binair", "hex", "base64"]).

[SOLUTION.md](SOLUTION.md)
