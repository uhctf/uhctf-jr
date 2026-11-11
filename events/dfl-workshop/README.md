# DFL-workshop security

- Doelgroep: leerlingen 3e graad secundair (16–18 jaar)
- Formaat: een groep leerlingen die in twee ploegen strijdt, Cyaan tegen Magenta. Binnen elke ploeg werken teams van 2 à 3 leerlingen, elk op een eigen laptop
- Duur: ongeveer 3 uur, met een pauze

Elk team werkt op een eigen laptop met de laptopmap: een startpagina met alle opdrachten, de decoder en de kluis. Er is geen internet of server nodig. Elk antwoord gaat in de kluis en opent een slot. **De kluis gaat open na 10 van de 14 sloten.** De laatste drie opdrachten zijn extra, voor teams die snel klaar zijn. Cyaan en Magenta strijden tegen elkaar: zie Score. De eerste 10 sloten zijn bewust geen programmeerwerk: de 16-jarigen leren nog maar net programmeren, dus de focus ligt op logisch denken en op eenvoudige onderzoeksopdrachten zoals Inspect Element. De extra opdrachten zijn voor leerlingen die in hun vrije tijd al veel met IT bezig zijn: ze zoeken zelf uit hoe ze verder komen en mogen daarbij ook code schrijven.

## Verloop (3 uur)

| Wanneer | Wat |
| --- | --- |
| 0:00–0:15 | welkom, wat is ethisch hacken (en wat niet), de afspraken, de kluis tonen. **Kies je kant** (5 min): iedereen leest de kleur van zijn kaartje af en zoekt de anderen met dezelfde kleur, zonder die hardop te zeggen. Zo ontstaan Cyaan en Magenta. Daarna teams van 2 à 3 binnen elke ploeg en de teamnaam invullen |
| 0:15–1:20 | blok 1: de teams werken zelf aan de laptopopdrachten. Cyaan komt in dit blok langs het lockpickingstation (zie de planning onder de tabel) |
| 1:20–1:35 | pauze |
| 1:35–2:40 | blok 2: verder met de laptopopdrachten. Magenta komt in dit blok langs het lockpickingstation |
| 2:40–3:00 | bespreking per opdracht (zie hieronder) en de stand |

Lockpicking loopt de hele tijd als station aan een aparte tafel: elk team komt één keer langs (ongeveer 15 minuten), op een moment dat de begeleider van het station kiest, binnen het blok van zijn ploeg. Het station telt niet mee voor de score.

Er zijn 14 sloten en de kluis gaat open na 10. De eerste 10 sloten kosten samen ongeveer 100 à 140 minuten, op 130 minuten werktijd, dus er is voor de meeste teams geen overschot. Elke extra opdracht kost 15 à 25 minuten. Een open slot telt mee voor de kluis, ook als het van een extra opdracht komt: een team dat vastzit bij een moeilijke opdracht kan dus een extra opdracht doen, en snelle teams kunnen er meer dan drie sloten bijnemen. Geef de extra opdrachten niet aan teams die achterlopen. Dat is krap: de makkelijke opdrachten (Romeinse geheimen, Phishing of echt?) zijn bedoeld om snel af te vinken, dus laat teams niet te lang blijven hangen en geef hints voor ze vastlopen. Staat een team om 2:20 nog niet ver, dan mogen de begeleiders de laatste opdracht samen met het team doen, zodat iedereen de kluis kan openen.

## Uitdagingen

De uitdagingen en de antwoorden van dit event staan in [event.toml](event.toml). Bouw alles met `./jr event build dfl-workshop`.

| Uitdaging | Niveau | Sloten | Wat leren ze |
| --- | --- | --- | --- |
| [Kies je kant](../../challenges/kies-je-kant/) | intro | – | een hexadecimale kleurcode (rood, groen, blauw) lezen om je kleur te vinden, en de anderen met dezelfde kleur zoeken. Zo ontstaan de twee ploegen. Op papier, zonder slot |
| [Romeinse geheimen](../../challenges/romeinse-geheimen/) | opwarmer | 1 | het Caesarcijfer (ROT-N): zoek de verschuiving met de oefenwoorden (huisdieren) en lees het bericht. Het caesarwiel op het scherm is een hulpmiddel: ze stellen de verschuiving in en tikken zelf woorden in om te vertalen |
| [Laag na laag](../../challenges/laag-na-laag/) | opwarmer | 1 | Base64, hexadecimaal, binair en ROT13 in vier lagen; coderen is geen versleutelen. De decoder doet het werk |
| [Robot-QR](../../challenges/robot-qr/) | opwarmer | 1 | kleurkanalen bewerken (Alleen blauw + Inverteren) tot een bijna onzichtbare QR-code leesbaar wordt |
| [Webvlaggen](../../challenges/webvlaggen/) | opwarmer tot gemiddeld | 3 | Inspect Element: paginabron, ontwikkelaarstools en bestanden die een site laadt. Elke vlag is een eigen slot |
| [Phishing of echt?](../../challenges/phishing-of-echt/) | makkelijk | 1 | nep- en echte berichten herkennen aan rode vlaggen (afzender, link, druk, belofte). De letters van de nepberichten spellen het antwoord. De teksten zijn geschreven voor jongere kinderen: laat ze er vlot doorheen gaan |
| [Wie is de hacker?](../../challenges/wie-is-de-hacker/) | logica | 1 | deductie: 8 verdachten, 6 verklaringen van getuigen. Eén aanwijzing is nooit genoeg |
| [Wachtwoord-mastermind](../../challenges/wachtwoord-mastermind/) | logica | 1 | het wachtwoord van een profiel raden met de feedback per vak (juist, fout, verkeerde plaats). Een wachtwoord uit je profiel is niet veilig |
| [Verborgen bestanden](../../challenges/verborgen-bestanden/) | moeilijkst | 1 | forensics met de bestandsinspecteur: magic bytes, een bestand met een valse extensie, gegevens na het einde van een foto |
| [Matroesjka](../../challenges/matroesjka/) | gemiddeld | 1 | forensics: een zip-bestand achter een foto geplakt. Een bestand is meer dan wat je programma toont: ze hernoemen `vakantiefoto.png` naar `.zip` en pakken het uit. Het bestand staat in `out/matroesjka/`, niet in de laptopmap |
| [Hack het portaal](../../challenges/hack-het-portaal/) | extra, gemiddeld tot moeilijk | 1 | webbeveiliging 2: een nep-leerlingenportaal testen. Een wazige laag wegnemen (Elementen), een nummer in de URL wijzigen en de rol in een Base64-token aanpassen. Vervolg op Webvlaggen: nu wijzigen in plaats van lezen. Het antwoord is een zin van 3 testwoorden |
| [Luister naar de stilte](../../challenges/luister-naar-de-stilte/) | extra, moeilijk | 1 | een WAV die stilte lijkt, maar morse bevat boven 16 kHz, naast een lokvogel op een hoorbare toon. De WAV-decoder toont golfvorm en spectrogram; de punten en strepen lezen ze zelf af en ze zetten ze om met de morsetabel of de decoder |
| [Hash-kraker](../../challenges/hash-kraker/) | extra, moeilijk | 1 | een lek met hashes (MD5, SHA-1, SHA-256) en een zout: het wachtwoord van de beheerder vinden met een hash-lab en zelf bedachte pogingen. Wie wil, schrijft code in het kladblok. Geen woordenlijstaanval ingebouwd: ze zoeken het zelf uit |
| [Lockpicking](../../challenges/lockpicking/) | station | – | hoe sloten werken, fysieke beveiliging. Zonder vlag, onder toezicht |

Kraak de code en Vigenère zitten niet meer in dit event, omdat ze programmeren of veel handwerk vragen. Ze staan nog in [challenges/](../../challenges/) voor een ouder publiek.

## De laptopmap

`./jr event build dfl-workshop` maakt naast de pdf's ook `events/dfl-workshop/out/laptop/`:

- `index.html`: de startpagina met teamnaam, een tegel per opdracht en de hulpmiddelen.
- een map per opdracht. Romeinse geheimen is een caesarwiel, Phishing of echt? laat je rode vlaggen aanvinken, Robot-QR is de beeldbewerker met de afbeelding, Verborgen bestanden heeft een bestandsinspecteur (hex, tekst, afbeelding), Wie is de hacker? en Wachtwoord-mastermind zijn spelbaar op het scherm, Webvlaggen is de nepwebsite zelf, Hack het portaal een nep-leerlingenportaal, Luister naar de stilte de WAV-decoder met het geluid erin en Hash-kraker een lek met een hash-lab en een kladblok.
- `kluis/index.html`: de kluis. Elk goed antwoord opent een slot (webvlaggen telt drie keer). De antwoorden staan enkel als hash in de pagina. De knop "Nieuw team (begeleider)" wist alles voor het volgende team.
- `decoder/index.html`: de decoder, voor Laag na laag (en voor de morse van Luister naar de stilte en de Base64-token van Hack het portaal).

Elk team heeft een eigen laptop. De papieren bladen en `out/verborgen-bestanden/usb/` (voor eigen gereedschap) helpen om tussendoor verder te werken.

## Voorbereiding

1. Bouw alles één keer: `./jr event build dfl-workshop`. Print alles uit dezelfde bouw.
2. Kopieer `out/laptop/` (bv. met een USB-stick) naar elke laptop. Open `index.html` in Chrome (of Edge) en maak er een bladwijzer van. Firefox houdt de opslag van pagina's vanaf schijf soms per map apart: dan ziet de startpagina de open sloten van de kluis niet.
3. Test de kluis met een paar antwoorden uit `ANTWOORDEN.pdf`, ga terug naar de startpagina en kijk of de sloten daar ook open staan. Druk daarna in de kluis op "Nieuw team".
4. Test Robot-QR op elke laptop: klik in de beeldbewerker op "Alleen blauw" en daarna op "Inverteren" en scan het scherm met een telefoon, met de schermhelderheid op maximum. Zet daarna alles terug met "Terugzetten".
5. Print de kaartjes van Kies je kant (zwart-wit volstaat) en knip ze uit (`kies-je-kant/deelnemer.pdf`, 10 kaartjes, genoeg voor maximaal 10 deelnemers; pas `aantal` aan als je er meer hebt) en leg ze in de volgorde van de stapel klaar.
6. Test de extra opdrachten in Chrome of Edge op elke laptop. Hack het portaal: open de ontwikkelaarstools (F12), controleer dat tabblad Application > Local Storage de sleutel `opdracht-portaal-token` toont en dat "Sessie herstellen" onderaan werkt. Luister naar de stilte: de pagina rekent een paar seconden bij het openen (spectrogram); geluid is niet nodig. Hash-kraker: typ `123456` in de hash-lab en controleer dat `sofie` gekraakt wordt. Druk daarna in de kluis op "Nieuw team": dat wist ook wat de opdrachten onthouden.
7. Zet `out/matroesjka/vakantiefoto.png` op elke laptop (bv. op het bureaublad, schrijfbaar) en controleer grootte en SHA-256 met `out/matroesjka/begeleider.pdf`. Toon bestandsextensies in Verkenner (Beeld > Weergeven > Bestandsnaamextensies) en test of hernoemen naar `.zip` en uitpakken lukt. Verstuur het bestand niet via chat of mail: dan verdwijnt de zip.
8. Optioneel per team een pakket op papier: de `deelnemer.pdf` van Verborgen bestanden (tabel met magic bytes).

## Materiaal

- per team: een laptop met de laptopmap, en minstens één smartphone met een QR-lezer (voor Robot-QR). Vraag vooraf aan de school of de leerlingen hun gsm mogen gebruiken, of neem enkele reservetoestellen mee
- de kaartjes van Kies je kant, pennen en kladpapier
- voor de begeleiders: `ANTWOORDEN.pdf` en de `begeleider.pdf`'s, met de hints en de oplossing
- lockpicking-sets en oefensloten, bij voorkeur doorzichtige (zie [Lockpicking](../../challenges/lockpicking/))

## Score

Cyaan en Magenta strijden tegen elkaar. Elk team werkt met een eigen laptop en moet 10 van de 14 sloten open krijgen; dan gaat de kluis open en kan het het diploma afdrukken.

- De ploeg met het hoogste **gemiddelde aantal open sloten per team** wint. Zo telt een ploeg met één team meer niet zwaarder.
- Hebben alle teams van een ploeg de kluis open, dan noteren de begeleiders het uur. Bij gelijkstand wint de ploeg die het eerst volledig klaar was.
- Noteer onderweg op het scoreblad achteraan `kies-je-kant/begeleider.pdf` per team het aantal open sloten (de lijst onder de sloten in de kluis) en het uur van de open kluis.
- Zet de twee ploegen aan aparte kanten van het lokaal, zodat ze elkaars laptops niet kunnen zien. Teams binnen één ploeg mogen elkaar wel helpen: zo wint de ploeg samen.

## Bespreking (laatste 20 minuten)

Overloop per opdracht kort wat erachter zit:

- **Kies je kant:** een kleur op je scherm is niets anders dan drie getallen in hexadecimaal. Computers werken met getallen, ook voor beelden. Ze vonden elkaar zonder dat iemand zijn kleur zei, en de achtergrond zei niets: je moet de data lezen, niet het uiterlijk.
- **Romeinse geheimen:** het Caesarcijfer is duizenden jaren oud en met 25 mogelijke verschuivingen in een paar minuten te kraken. Een gekend woord (de oefenwoorden) verraadt de sleutel.
- **Laag na laag:** Base64, hex, binair en ROT13 verbergen niets: iedereen kan ze terugdraaien. Coderen is geen versleutelen. *Defense in depth* werkt alleen met echte beveiligingslagen.
- **Robot-QR:** "onzichtbaar voor het oog" is niet "verborgen" voor een computer. Kijk naar de data, niet naar wat je ziet.
- **Webvlaggen:** alles wat een website naar je browser stuurt, kan je lezen: broncode, commentaar en geladen bestanden. Geheimen horen niet in de browser.
- **Phishing of echt?:** nepberichten spelen in op haast, angst of een te mooie belofte. Kijk naar de afzender en de link, en klik niet zomaar.
- **Wie is de hacker?:** één aanwijzing is nooit genoeg, samen vertellen ze het verhaal. Zo werken onderzoekers ook met logbestanden.
- **Wachtwoord-mastermind:** een wachtwoord dat uit je profiel te halen is, is niet veilig. Aanvallers proberen eerst wat ze over je kunnen vinden.
- **Verborgen bestanden:** een extensie is maar een naam. Virusscanners en e-mailfilters kijken naar de inhoud, en onderzoekers ook.
- **Hack het portaal:** alles wat in de browser staat, kan een gebruiker aanpassen: een wazige laag, een nummer in de URL, een token in Local Storage. Een server moet bij elke aanvraag controleren wie je bent en wat je mag, en een token heeft een handtekening die de server controleert. Dat deden we hier enkel in een simulatie en nooit bij echte sites zonder toestemming.
- **Luister naar de stilte:** onhoorbaar is niet afwezig, net als onzichtbaar niet verborgen is (Robot-QR). Informatie verstoppen in geluid heet steganografie. En een lokvogel kost je tijd: het eerste dat je vindt, is niet altijd het antwoord.
- **Hash-kraker:** een hash is een vingerafdruk en geen versleuteling, maar zwakke wachtwoorden raad je toch. Een zout maakt algemene opzoektabellen nutteloos, trage hashes (bcrypt, Argon2) maken het raden duur en een wachtwoord uit een patroon (woord plus jaartal) blijft zwak. Op Have I Been Pwned kun je zien of je gegevens ooit lekten.
- **Matroesjka:** een extensie is maar een naam en een bestand kan een ander bestand verbergen: de foto opent gewoon, maar als zip komt er een geheim uit. Zo verstoppen aanvallers gegevens of malware in onschuldige bestanden.
- **Lockpicking:** fysieke beveiliging telt ook mee: een sterk wachtwoord helpt niet als iemand de serverkamer binnen kan.

## Opzet en tips

- Alle teams hebben dezelfde opdrachten en antwoorden. Omdat de ploegen tegen elkaar strijden, vraag je ze de antwoorden niet door te geven aan de andere ploeg.
- Spreek de afspraken van ethisch hacken expliciet af: oefenen enkel op eigen materiaal of met toestemming.
- Kies je kant: deel de kaartjes één voor één uit in de volgorde van de stapel, dan zijn de ploegen even groot. Ze mogen elkaars kaartjes bekijken maar de kleur niet hardop zeggen. Controleer daarna met `begeleider.pdf` of iedereen goed staat. Vertel pas dan dat Cyaan en Magenta tegen elkaar strijden en wanneer elke ploeg langs het lockpickingstation gaat.
- Romeinse geheimen: wie de verschuiving niet vindt, laat je de oefenwoorden (huisdieren) eerst intikken in het caesarwiel. Dat is de sleutel voor het echte bericht.
- Phishing of echt?: de berichten zijn gemaakt voor kinderen van 10 à 11 jaar. Dat is niet erg: het is een snelle opdracht om de teams op gang te brengen.
- Laag na laag: de laatste laag (ROT13) herkennen ze niet aan het uiterlijk. De vierde hint in de pagina zet ze op weg naar ROT-N in de decoder.
- Webvlaggen: de derde vlag staat in een taalbestand dat de pagina niet laadt. Wie in het tabblad Netwerk enkel `nl.js` en `en.js` ziet, moet zelf `fr.js` proberen; de uitgecommentarieerde FR-knop in de bron is de aanwijzing.
- Wie is de hacker?: wie vastzit, laat je de verklaringen één voor één afvinken en de verdachten schrappen die niet meer passen.
- Verborgen bestanden is de moeilijkste opdracht en kost 20 à 30 minuten. Let erop dat teams er in blok 2 niet te laat aan beginnen.
- Matroesjka: laat teams eerst de bestandsgrootte van de foto bekijken (te groot voor zo'n kleine foto). Staan de extensies niet zichtbaar, dan wordt hernoemen `vakantiefoto.zip.png` en werkt het niet.
- Hack het portaal: wie de rol niet vindt, laat je de token in Local Storage zoeken (Application in Chrome en Edge, Opslag in Firefox) en het deel voor de punt in de decoder omzetten. Maakt een team iets stuk, dan zet "Sessie herstellen" onderaan alles terug.
- Luister naar de stilte: laat teams niet allemaal geluid afspelen, het werkt met de ogen. Wie enkel de golfvorm versterkt, vindt de lokvogel en typt een fout antwoord. De hint over "meer dan een rij" zet hen op weg.
- Hash-kraker: laat ze eerst zelf uitzoeken wat een hash is en hoe je er een kraakt. De hints in de pagina doen de rest. Wie het zout vergeet, krijgt een andere hash: dat is de les. De woordenlijst in het kladblok (`WOORDEN`) staat pas in de laatste hint.
- Spreek het lockpicking-station af met een volwassene aanwezig.
