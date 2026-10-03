<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Webvlaggen

- Author: UHCTF

- Format: booth

- Age: 12–18

- Duration: 15–20 min

- Topic: Webpagina's bekijken, bronnen en bestanden, talen

- Materials: laptop met browser, Python 3 (`python3 -m http.server` in [src/](src/))

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>web 1 (makkelijk): <code>web-not-so-hidden</code></li>
<li>web 2 (moeilijk): <code>web-flag-in-transit</code></li>
<li>web 3 (extreem): <code>le-langue-secrete</code></li>
</ul></ul></details>

## Beschrijving

Op de website van de Open Dag staat een gratis flag, maar die is niet altijd zichtbaar. Er zijn drie vlaggen te vinden, in oplopende moeilijkheid:

1. **De "verborgen" webvlag.** De website probeert enkele vlaggen te verbergen, er was er een die niet meteen werd gezien. Tip: de inhoud begint met `web-n`.
2. **De standaardvlag.** Men zou zich kunnen afvragen welke vlag wordt weergegeven als er geen taal is geselecteerd. Tip: de inhoud begint met `web-f`.
3. **De meertalige vlag.** De website is beschikbaar in meerdere talen, maar de vlag lijkt in de meeste ervan gecensureerd. Tip: zoek in een andere taal.

## Hints

1. Een browser kan de broncode van een pagina tonen (rechtsklik, 'Paginabron weergeven', of Ctrl+U).
2. Zoek in de bron naar 'flag'. Kijk ook naar commentaar en naar wat er staat voordat de taal geladen wordt.
3. De tekst van de pagina komt uit bestanden per taal. Kijk in het tabblad Netwerk van de ontwikkelaarstools welk bestand geladen wordt, en probeer een andere taal.

## Opzet

Start in [src/](src/) een lokale server: `python3 -m http.server` en open `http://localhost:8000`. Openen vanaf schijf werkt niet, omdat de pagina taalbestanden inlaadt met `fetch`. De pagina gebruikt geen externe bibliotheken en werkt offline.

Dit is een statische uitdaging: het materiaal staat vast en er is geen event-specifieke versie. `./jr event build` kopieert `src/` ongewijzigd.

[SOLUTION.md](SOLUTION.md)
