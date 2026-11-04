# Oplossing

1. **web 1:** in de broncode staat bij de eerste kaart een HTML-commentaar `<!-- Vlag 1: web-not-so-hidden -->`.
2. **web 2:** de standaardtekst in de HTML (voordat het taalbestand de tekst vervangt door `[GECENSUREERD]`) is `web-flag-in-transit`. Zichtbaar via de paginabron, of met JavaScript uitgeschakeld.
3. **web 3:** de pagina laadt `taal/en.js` of `taal/nl.js` (zichtbaar in het tabblad Netwerk, of in de bron). In de bron staat ook een uitgecommentarieerde knop voor Frans. Open `taal/fr.js` zelf: daar staat `"ctf.flag": "la-langue-secrete"`.

> Opmerking bij hergebruik: in 2025 stond voor web 1 de bijhorende vlag niet in de pagina zelf. Deze versie plaatst hem in een commentaar, zodat de uitdaging oplosbaar is.
