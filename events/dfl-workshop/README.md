# DFL-workshop security

- Doelgroep: leerlingen 3e graad secundair (16–18 jaar)
- Formaat: workshop in groepen van 6 à 8 leerlingen, verdeeld in teams van 2 à 3
- Duur: ongeveer 3 uur, met een pauze

Elk team werkt op een laptop met de laptopmap: een startpagina met alle opdrachten, de decoder en de kluis. Er is geen internet of server nodig. Elk antwoord gaat in de kluis; met 5 van de 8 sloten gaat ze open. Er zijn bewust meer opdrachten dan tijd, en de laatste zijn echt moeilijk.

## Verloop (3 uur)

| Wanneer | Wat |
| --- | --- |
| 0:00–0:15 | welkom, wat is ethisch hacken (en wat niet), de afspraken, de kluis tonen, teams maken en teamnaam invullen |
| 0:15–1:20 | blok 1: de teams kiezen zelf. Raad de opwarmers aan om te starten (Laag na laag, Robot-QR, Webvlaggen) |
| 1:20–1:35 | pauze |
| 1:35–2:40 | blok 2: de moeilijke opdrachten (Kraak de code, Vigenère, Verborgen bestanden) |
| 2:40–3:00 | bespreking per opdracht (zie hieronder) en de stand |

Lockpicking loopt de hele tijd als station aan een aparte tafel: elk team komt één keer langs (ongeveer 15 minuten), op een moment dat de begeleider van het station kiest.

## Uitdagingen

De uitdagingen en de antwoorden van dit event staan in [event.toml](event.toml). Bouw alles met `./jr event build dfl-workshop`.

| Uitdaging | Niveau | Sloten | Wat leren ze |
| --- | --- | --- | --- |
| [Laag na laag](../../challenges/laag-na-laag/) | opwarmer | 1 | Base64, hexadecimaal, binair en ROT13 in vier lagen; coderen is geen versleutelen |
| [Robot-QR](../../challenges/robot-qr/) | opwarmer | 1 | kleurkanalen bewerken tot een bijna onzichtbare QR-code leesbaar wordt. Donkerder dan standaard (`#000014`) |
| [Webvlaggen](../../challenges/webvlaggen/) | opwarmer tot gemiddeld | 3 | paginabron, ontwikkelaarstools en bestanden die een site laadt. Elke vlag is een eigen slot |
| [Kraak de code](../../challenges/kraak-de-code/) | moeilijk | 1 | recursie en efficiënte algoritmen. Code(40) en Code(70): de functie rechtstreeks uitvoeren duurt te lang, dus moeten ze een lus of memoization bedenken. Op de laptop met een JavaScript-kladblok |
| [Vigenère](../../challenges/vigenere/) | moeilijk | 1 | een klassiek cijfer kraken met een aanval met bekende klare tekst. Sleutel `HACKER` |
| [Verborgen bestanden](../../challenges/verborgen-bestanden/) | moeilijk | 1 | forensics: magic bytes, een bestand met een valse extensie, gegevens na het einde van een foto |
| [Lockpicking](../../challenges/lockpicking/) | station | – | hoe sloten werken, fysieke beveiliging. Zonder vlag, onder toezicht |

## De laptopmap

`./jr event build dfl-workshop` maakt naast de pdf's ook `events/dfl-workshop/out/laptop/`:

- `index.html`: de startpagina met teamnaam, een tegel per opdracht en de hulpmiddelen.
- een map per opdracht. Robot-QR is de beeldbewerker met de afbeelding, Kraak de code heeft een JavaScript-kladblok, Verborgen bestanden heeft een bestandsinspecteur (hex, tekst, afbeelding), Webvlaggen is de nepwebsite zelf.
- `kluis/index.html`: de kluis. Elk goed antwoord opent een slot (webvlaggen telt drie keer). De antwoorden staan enkel als hash in de pagina. De knop "Nieuw team (begeleider)" wist alles voor het volgende team.
- `decoder/index.html`: de decoder, voor Laag na laag.

Liefst heeft elk team een eigen laptop. Met één laptop per groep wordt de laptop een station waar de teams om beurten komen. De papieren bladen en `out/verborgen-bestanden/usb/` (voor eigen gereedschap) helpen dan om tussendoor verder te werken.

## Voorbereiding

1. Bouw alles één keer: `./jr event build dfl-workshop`. Print alles uit dezelfde bouw.
2. Kopieer `out/laptop/` (bv. met een USB-stick) naar elke laptop. Open `index.html` in Chrome (of Edge) en maak er een bladwijzer van. Firefox houdt de opslag van pagina's vanaf schijf soms per map apart: dan ziet de startpagina de open sloten van de kluis niet.
3. Test de kluis met een paar antwoorden uit `ANTWOORDEN.pdf`, ga terug naar de startpagina en kijk of de sloten daar ook open staan. Druk daarna in de kluis op "Nieuw team".
4. Test Robot-QR op elke laptop: zet in de beeldbewerker Blauw hoog en Inverteren op 100 % en scan het scherm met een telefoon. Zet daarna alles terug.
5. Maak per team een pakket op papier: de `deelnemer.pdf` van Vigenère (met de Vigenèretabel), Verborgen bestanden (tabel met magic bytes), Kraak de code en Robot-QR.

## Materiaal

- per team: een laptop met de laptopmap, en minstens één smartphone met een QR-lezer (voor Robot-QR)
- het pakket op papier (zie Voorbereiding), pennen en kladpapier
- voor de begeleiders: `ANTWOORDEN.pdf` en de `begeleider.pdf`'s, met de hints en de oplossing
- lockpicking-sets en oefensloten, bij voorkeur doorzichtige (zie [Lockpicking](../../challenges/lockpicking/))

## Score

De stand is het aantal open sloten in de kluis van elk team (de lijst onder de sloten). Bij gelijkstand wint het team dat de kluis het eerst open had: de begeleiders noteren het uur waarop een team de kluis opent. Wie de kluis open heeft, kan het diploma afdrukken.

## Bespreking (laatste 20 minuten)

Overloop per opdracht kort wat erachter zit:

- **Laag na laag:** Base64, hex en ROT13 verbergen niets: iedereen kan ze terugdraaien. Coderen is geen versleutelen. *Defense in depth* werkt alleen met echte beveiligingslagen.
- **Robot-QR:** "onzichtbaar voor het oog" is niet "verborgen" voor een computer. Kijk naar de data, niet naar wat je ziet.
- **Webvlaggen:** alles wat een website naar je browser stuurt, kan je lezen: broncode, commentaar en geladen bestanden. Geheimen horen niet in de browser.
- **Kraak de code:** dezelfde functie kan seconden of eeuwen duren, afhankelijk van het algoritme. Daarom kies je in cryptografie problemen waarvoor geen snelle aanpak bestaat.
- **Vigenère:** een sleutel die zich herhaalt en een voorspelbaar begin breken het cijfer. Het principe van Kerckhoffs: een systeem moet veilig blijven, ook als iedereen weet hoe het werkt. Enkel de sleutel is geheim.
- **Verborgen bestanden:** een extensie is maar een naam. Virusscanners en e-mailfilters kijken naar de inhoud, en onderzoekers ook.
- **Lockpicking:** fysieke beveiliging telt ook mee: een sterk wachtwoord helpt niet als iemand de serverkamer binnen kan.

## Opzet en tips

- Alle teams hebben dezelfde opdrachten en antwoorden. Vraag ze de antwoorden voor zich te houden.
- Spreek de afspraken van ethisch hacken expliciet af: oefenen enkel op eigen materiaal of met toestemming.
- Kraak de code: wie de functie rechtstreeks in het kladblok uitvoert met 70, laat de pagina vastlopen. Dat is de bedoeling: herlaad de pagina en geef de hint over memoization. Code(70) past nog exact in een JavaScript-getal.
- Vigenère: teams die vastzitten, laat je de eerste letters van het bericht onder het bekende begin schrijven. Het patroon `HACKER HACKER` valt dan snel op.
- Spreek het lockpicking-station af met een volwassene aanwezig.
