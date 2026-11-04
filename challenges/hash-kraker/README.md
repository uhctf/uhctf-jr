<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Hash-kraker

- Author: UHCTF

- Format: booth

- Age: 15–18

- Duration: 15–25 min

- Topic: Hashes, wachtwoorden kraken, zout, veilig wachtwoordgebruik

- Materials: laptop met de digitale pagina (het lek, de hash-lab en het kladblok); `deelnemer.pdf` is een korte opdracht

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>voetbal2017</code></li>
</ul></ul></details>

## Beschrijving

Een webwinkel is gehackt. De aanvallers hebben de lijst met accounts gestolen, met een hash in plaats van een wachtwoord. Een hash is een vingerafdruk van een wachtwoord: je kunt hem niet omdraaien. Of toch niet? Vind het wachtwoord van de beheerder.

## Hints

1. Een hash is een vingerafdruk van een wachtwoord: je kunt hem niet omdraaien. Maar je kunt wel zelf wachtwoorden hashen en kijken of de vingerafdruk gelijk is.
2. Tel de tekens van een hash: 32 is MD5, 40 is SHA-1, 64 is SHA-256. De hash-lab rekent ze alle drie uit en vergelijkt met het lek. Begin met de geheugensteuntjes.
3. Mensen gebruiken eenvoudige patronen: een woord, een jaartal, een hoofdletter, '01'. Kijk ook naar de kolom aangemaakt.
4. De beheerder heeft een zout. Dat is een stukje tekst dat voor het wachtwoord gezet wordt voordat er gehasht wordt. Probeer zout en wachtwoord als één tekst.
5. Veel wachtwoorden proberen? Schrijf code in het kladblok: WOORDEN is een lijst woorden en md5(), sha1() en sha256() rekenen hashes uit.

## Opzet

De deelnemers krijgen een lek van een verzonnen webwinkel (`lek.csv`, ook als tabel in de digitale pagina) met vijf accounts en de kolommen gebruiker, e-mail, hash, zout, aangemaakt en geheugensteuntje. Ze moeten **zelf uitzoeken** hoe ze verder komen: de pagina rekent geen wachtwoorden voor hen uit en bevat geen woordenlijstaanval.

De **hash-lab** rekent live MD5, SHA-1 en SHA-256 uit van wat een team typt en vergelijkt elke hash met het lek. Een treffer wordt gemarkeerd en onthouden. Voor wie wil programmeren is er een **kladblok (JavaScript)** met `md5()`, `sha1()`, `sha256()`, `LEK` en `WOORDEN` (een lijst woorden, enkel genoemd in de laatste hint).

De accounts zijn een trap van moeilijkheid: `sofie` (MD5, een van de meest gebruikte wachtwoorden), `tom` (MD5, een woord), `lotte` (MD5, een seizoen met jaartal), `jan` (SHA-1, hoofdletter en cijfers) en `beheerder` (SHA-256 met een zout). Het antwoord is het wachtwoord van de beheerder: het woord van Tom plus het jaar waarin de winkel begon (de kolom aangemaakt). De trucjes zitten in de steuntjes. Wie het zout vergeet, krijgt een andere hash en vindt niets: dat is het slot van deze opdracht. De pagina vergelijkt de ingetypte tekst letterlijk, dus een team moet zelf zout en wachtwoord aan elkaar plakken.

Het antwoord moet een woord met een jaartal zijn, en dat woord moet in `woorden.txt` staan, zodat de zelftest bevestigt dat het met de aanpak uit de hints te vinden is. Met `seed` veranderen de zouten, het seizoen van Lotte en de datums.

Bespreking: een hash is geen versleuteling maar een vingerafdruk. Daarom is het toch raden als de wachtwoorden zwak zijn. Een zout maakt een algemene opzoektabel nutteloos, en trage hashes (bcrypt, Argon2) maken het raden veel duurder. Een wachtwoord dat uit een patroon komt (woord plus jaartal), of hetzelfde wachtwoord op meerdere plaatsen, blijft zwak. Wie wil weten of zijn eigen gegevens ooit lekten, kan dat controleren op Have I Been Pwned.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build hash-kraker
```

Voor een event met een eigen antwoord:

```
./jr event add <event> hash-kraker --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `winkel` ("SportHoek"), `digitaal` (true).

[SOLUTION.md](SOLUTION.md)
