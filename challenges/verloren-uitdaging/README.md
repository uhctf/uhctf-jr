<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# De verloren uitdaging

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: URL's, foutmeldingen lezen

- Materials: laptop, Python 3 (voor [src/server.py](src/server.py))

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>antwoord: <code>work-in-progress-flag</code></li>
</ul></ul></details>

## Beschrijving

Er was hier vroeger een uitdaging, maar die lijkt te ontbreken. Kun je hem vinden?

## Hints

1. Foutmeldingen proberen je meestal te helpen.
2. Lees goed welk adres er precies gevraagd werd. Zie je een verschil met wat je verwacht?
3. Sommige hoofdletters en kleine letters lijken sterk op elkaar (`I` en `l`). Probeer het adres met kleine letters.

## Opzet

Start de server met `python3 server.py` in de map [src/](src/) en open `http://localhost:8000`. De server toont bij een onbekende pagina een foutmelding met details van het verzoek. Zonder server werkt de foutmelding niet.

Dit is een statische uitdaging: het materiaal staat vast en er is geen event-specifieke versie. `./jr event build` kopieert `src/` ongewijzigd.

[SOLUTION.md](SOLUTION.md)
