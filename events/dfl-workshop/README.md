# DFL-workshop security

- Doelgroep: leerlingen 3e graad secundair
- Formaat: workshop in groepen van 6 à 8 leerlingen
- Duur: ongeveer 3 uur

## Uitdagingen

De uitdagingen en onze eigen antwoorden staan in [uitdagingen.toml](uitdagingen.toml). Bouw de pdf's en pagina's met `./jr event build dfl-workshop`.

| Uitdaging | Leeftijd | Type | Wat leren ze |
| --- | --- | --- | --- |
| [De verloren uitdaging](../../challenges/verloren-uitdaging/) | 8–12 | statisch | foutmeldingen en URL's lezen (opwarmer) |
| [Kraak de code](../../challenges/kraak-de-code/) | 12–15 | gegenereerd | recursie. Hier rekenen ze Code(12) en Code(15) uit. |
| [Laag na laag](../../challenges/laag-na-laag/) | 12–15 | gegenereerd | ROT13, binair, hexadecimaal en Base64 in lagen. Vier lagen in plaats van drie. |
| [Robot-QR](../../challenges/robot-qr/) | 12–15 | gegenereerd | afbeeldingen bewerken tot een verborgen QR-code leesbaar wordt. De QR scannen ze met hun smartphone. |
| [Webvlaggen](../../challenges/webvlaggen/) | 12–18 | statisch | broncode, ontwikkelaarstools en bestanden op een webpagina (3 vlaggen) |
| [Lockpicking](../../challenges/lockpicking/) | 12–18 | gegenereerd | hoe sloten werken, fysieke beveiliging. Zonder vlag, onder toezicht. |

## Materiaal

- smartphone van de leerlingen
- een laptop van de begeleiders als lokale webserver. Start in `events/dfl-workshop/out/` met `python3 -m http.server`, dan openen de leerlingen op hun smartphone `http://<ip-van-de-laptop>:8000/...` voor de decoder, de beeldbewerker en de webvlaggen. Dit vraagt wifi of een hotspot waarop de telefoons en de laptop zitten.
- afdrukken: de `deelnemer.pdf`'s uit `out/` (kraak de code, laag na laag, robot-qr) plus `ANTWOORDEN.pdf` en de `begeleider.pdf`'s voor de begeleiders
- lockpicking-sets en oefensloten (zie [Lockpicking](../../challenges/lockpicking/))

## Score

Nog te bepalen.

## Opzet en tips

- Spreek het lockpicking-station af met een volwassene aanwezig.
