# Oplossing

1. **web 1:** in de broncode staat bij de eerste kaart een HTML-commentaar `<!-- Vlag 1: web-not-so-hidden -->`.
2. **web 2:** de standaardtekst in de HTML (vóór de taalbestanden de tekst vervangen door `[GECENSUREERD]`) is `web-flag-in-transit`. Zichtbaar via de paginabron, of met JavaScript uitgeschakeld.
3. **web 3:** de pagina laadt `taal/en.json` of `taal/nl.json`. Probeer `taal/fr.json` (Frans, in de code uitgecommentarieerd): daar staat `"ctf.flag": "le-langue-secrete"`.

> Opmerking bij hergebruik: in 2025 stond voor web 1 de bijhorende vlag niet in de pagina zelf. Deze versie plaatst hem in een commentaar, zodat de uitdaging oplosbaar is.
