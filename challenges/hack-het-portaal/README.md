<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Hack het portaal

- Author: UHCTF

- Format: booth

- Age: 15–18

- Duration: 15–25 min

- Topic: Webbeveiliging: elementen aanpassen, URL's wijzigen, sessiesleutels (tokens), wat de browser mag vertrouwen

- Materials: laptop met Chrome of Edge (ontwikkelaarstools), de Decoder; `deelnemer.pdf` is de opdrachtbrief

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>vertrouw-nooit-de-browser</code></li>
</ul></ul></details>

## Beschrijving

Het leerlingenportaal van een school staat online en niemand weet hoe veilig het is. Jullie mogen het testen. Er zijn drie testwoorden verstopt op plaatsen waar enkel leraren, de directie of beheerders mogen komen. Je bent ingelogd als een gewone leerling. Vind de drie woorden: samen vormen ze de zin voor de kluis.

## Hints

1. Je bent ingelogd als een gewone leerling. Zoek pagina's waar je niet mag komen en kijk wat de browser eigenlijk al gekregen heeft. Open de ontwikkelaarstools met F12.
2. Iets wazig of afgedekt? Wat je ziet is niet alles wat de browser kreeg. Kijk in het tabblad Elementen (Inspecteren) en pas de laag aan of lees de tekst.
3. De URL van je rapport bevat een nummer. Wie zegt dat dit nummer van jou is? Probeer een ander nummer. Wie heeft vast een laag nummer?
4. De beheerderspagina kijkt naar je sessiesleutel (token). Die staat in de ontwikkelaarstools, bij Toepassing (Chrome, Edge) of Opslag (Firefox), onder Local Storage.
5. Een token is vaak Base64. Zet het deel voor de punt in de Decoder om naar tekst en kijk bij 'rol'. Verander die, zet het terug om naar Base64 en plak het op dezelfde plaats.

## Opzet

Dit is het vervolg op Webvlaggen: daar lezen de leerlingen wat een site naar hun browser stuurt, hier **wijzigen** ze het. De site (`site/`, in de laptopmap `hack-het-portaal/`) is een nep-leerlingenportaal met drie fasen, elk met een eigen testwoord van het antwoord:

1. **Klasgemiddelde** (`klas.html`): de inhoud zit achter een wazige laag. De tekst staat gewoon in de pagina. Wie in Elementen kijkt, leest ze of verwijdert de laag.
2. **Mijn rapport** (`rapport.html?leerling=24`): het nummer in de adresbalk bepaalt wiens rapport je ziet. Leerling 1 is de directeur: zijn notitie bevat het tweede woord en verwijst naar de beheerpagina (een IDOR).
3. **Beheer** (`beheer.html`): de pagina kijkt naar de `rol` in de sessiesleutel (token) in Local Storage. Die token is Base64 van een stukje JSON, gevolgd door een punt en een handtekening die niemand controleert. Wie de rol in `beheerder` verandert, krijgt het derde woord. Dit sluit aan op Laag na laag: Base64 met de Decoder.

Het antwoord heeft minstens 3 woorden, het laatste deel krijgt de rest (bij het standaardantwoord: `vertrouw`, `nooit` en `de browser`). De woorden voor fase 2 en 3 zijn versleuteld met een sleutel die uit de aanvraag komt (het nummer, de rol): wie enkel de broncode leest, vindt ze niet, wie de aanvraag aanpast wel.

**Belangrijk bij de bespreking:** alles gebeurt in de browser, dus dit is een simulatie. Een echte site controleert toegang op de server en tekent een token met een geheim dat de gebruiker niet kent. De pagina zegt zelf in het commentaar dat de handtekening niet gecontroleerd wordt. Dit mag een leerling nooit bij een echte site proberen zonder toestemming.

Praktisch:

- Chrome of Edge werkt het best (tabblad Application). In Firefox heet dat Opslag. De pagina's slaan enkel de token op, onder `opdracht-portaal-token`; "Sessie herstellen" onderaan maakt een nieuwe als een team iets stuk maakt. "Nieuw team" in de kluis wist hem ook.
- Alle pagina's moeten in dezelfde map blijven, anders ziet de ene pagina de token van de andere niet (zie de opmerking over Firefox bij de laptopmap).
- Leerlingen die de token zelf in Base64 omzetten kunnen de handtekening weglaten: de pagina leest alleen het deel voor de punt.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build hack-het-portaal
```

Voor een event met een eigen antwoord:

```
./jr event add <event> hack-het-portaal --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `school` ("Zandberg College").

[SOLUTION.md](SOLUTION.md)
