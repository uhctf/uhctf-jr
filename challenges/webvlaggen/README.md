<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Webvlaggen

- Author: UHCTF

- Format: booth

- Age: 12–18

- Duration: 15–20 min

- Topic: Webpagina's bekijken, bronnen en bestanden, talen

- Materials: laptop met browser

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>web 1 (makkelijk): <code>web-not-so-hidden</code></li>
<li>web 2 (gemiddeld): <code>web-flag-in-transit</code></li>
<li>web 3 (moeilijker): <code>la-langue-secrete</code></li>
</ul></ul></details>

## Beschrijving

Op de website van de Open Dag staat een gratis flag, maar die is niet altijd zichtbaar. Er zijn drie vlaggen te vinden, in oplopende moeilijkheid:

1. **De "verborgen" webvlag.** De website probeert enkele vlaggen te verbergen, er was er een die niet meteen werd gezien. Tip: de inhoud begint met `web-n`.
2. **De standaardvlag.** Men zou zich kunnen afvragen welke vlag wordt weergegeven als er geen taal is geselecteerd. Tip: de inhoud begint met `web-f`.
3. **De meertalige vlag.** De website is beschikbaar in meerdere talen, maar de vlag lijkt in de meeste ervan gecensureerd. Tip: zoek in een andere taal.

## Hints

1. Een browser kan de broncode van een pagina tonen (rechtsklik, 'Paginabron weergeven', of Ctrl+U).
2. Zoek in de bron naar 'flag'. Kijk ook naar commentaar en naar wat er staat voordat de taal geladen wordt.
3. De tekst van de pagina komt uit een bestand per taal. Kijk in het tabblad Netwerk van de ontwikkelaarstools welk bestand geladen wordt, en open dat bestand zelf. Bestaat er nog een andere taal?

## Opzet

Open [src/index.html](src/index.html) in de browser. De pagina laadt haar teksten uit `taal/<taal>.js` met een scripttag, dus ze werkt vanaf schijf en via een webserver (`python3 -m http.server` in `src/`). Ze gebruikt geen externe bibliotheken en werkt offline. In een event met een laptopmap komt de site in `laptop/webvlaggen/` en telt elke vlag als een eigen slot in de kluis.

Dit is een statische uitdaging: het materiaal staat vast en er is geen event-specifieke versie. `./jr event build` kopieert `src/` ongewijzigd.

[SOLUTION.md](SOLUTION.md)
