<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Romeinse geheimen

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 5–10 min

- Topic: Caesarcijfer (ROT-N)

- Materials: geprint bericht (`deelnemer.pdf`), potlood; optioneel een laptop of tablet met de [decoder](../_gedeeld/decoder/) en de [spiekbrief](../_gedeeld/spiekbrief/)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>veni vidi vici</code></li>
</ul></ul></details>

## Beschrijving

Een archeoloog vond een bericht dat lijkt te zijn gecodeerd door een keizer.

Het bericht: `SBKF OBWB KXRX`

## Hints

1. Welke keizer gebruikte een geheimschrift waarbij je letters verschuift?
2. Het is een Caesarcijfer: in elk woord is elke letter een vast aantal plaatsen verschoven.
3. Bestaat het bericht uit meer woorden? Dan kan elk woord een andere verschuiving hebben. Zoek ze één voor één.
4. Probeer het met kleine getallen: verschuif 1, 2, 3 plaatsen.

## Opzet

Deelnemers gebruiken de strook op `deelnemer.pdf`, of de meegeleverde [decoder](../_gedeeld/decoder/) (lokaal in de browser, geen internet nodig). De [spiekbrief](../_gedeeld/spiekbrief/) kan er bij geprint worden. Zet `met_decoder = false` voor een versie volledig op papier. `verschuivingen` zijn de aantallen letters: één per woord van het antwoord, en ze verschillen. Met één getal (bv. `[3]`) geldt dezelfde verschuiving voor alle woorden. De deelnemers moeten dus per woord opnieuw zoeken. Met `oefenwoorden` (bv. `["kat", "hond"]`) en een `oefenhint` (bv. "Veel voorkomende huisdieren") komen er korte, makkelijk te raden woorden op het blad met dezelfde verschuiving: raad ze en je vindt de verschuiving, om daarna het moeilijkere bericht te ontcijferen. Bij meerdere verschuivingen hoort oefenwoord 1 bij woord 1, oefenwoord 2 bij woord 2, enzovoort. Het bericht staat ook in `bericht.txt`. Met `digitaal = true` komt er ook een hulpmiddel bij voor op een laptop (`digitaal.html`): een caesarwiel waarop de kinderen de verschuiving instellen en zelf woorden intikken om te laten vertalen. Er staat geen bericht of oefenwoord in de pagina: ze tikken zelf in wat ze op papier lezen. De verschuiving staat niet in de pagina zelf.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build romeinse-geheimen
```

Voor een event met een eigen antwoord:

```
./jr event add <event> romeinse-geheimen --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `verschuivingen` ([3, 7, 11]), `met_decoder` (true), `digitaal` (false), `oefenwoorden` ([]), `oefenhint` ("").

[SOLUTION.md](SOLUTION.md)
