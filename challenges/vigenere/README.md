<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Vigenère

- Author: UHCTF

- Format: booth

- Age: 15–18

- Duration: 20–30 min

- Topic: Klassieke cryptografie, Vigenèrecijfer, aanval met bekende klare tekst

- Materials: geprint bericht met Vigenèretabel (`deelnemer.pdf`), pen; of de digitale versie op een laptop

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>polyalfabetisch</code></li>
</ul></ul></details>

## Beschrijving

Een onderschept bericht van een geheim agent. Het is versleuteld met het Vigenèrecijfer: een Caesarcijfer waarbij de verschuiving per letter verandert, volgens een sleutelwoord dat zich herhaalt. De sleutel kennen we niet. Wel weten we hoe elk bericht van deze agenten begint.

## Hints

1. Zet de eerste letters van het bericht onder het begin dat je kent. Hoeveel plaatsen is elke letter verschoven?
2. Schrijf elke verschuiving als letter (0 = A, 1 = B, ...). Zie je een woord dat zich herhaalt? Dat is de sleutel.
3. Ontcijferen: schuif elke letter terug met de sleutelletter eronder. Spaties tellen niet mee voor de sleutel.

## Opzet

Het bericht wordt gemaakt uit `bekend`, een vaste tekst en het `antwoord`, en versleuteld met `sleutel`. Alleen letters worden versleuteld en de sleutel schuift enkel op bij letters; spaties blijven staan. Op het blad staan het bericht, het bekende begin en een Vigenèretabel. Deelnemers vinden de sleutel door het bekende begin met het bericht te vergelijken (een aanval met bekende klare tekst, zoals bij Enigma) en ontcijferen daarna de rest. Met `digitaal = true` komt er een pagina bij waarin ze een sleutel intypen en de ontcijfering meteen zien. De pagina zoekt de sleutel niet zelf. Na afloop: waarom is een sleutel die zich herhaalt zwak, en wat doet moderne cryptografie anders?

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build vigenere
```

Voor een event met een eigen antwoord:

```
./jr event add <event> vigenere --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `sleutel` ("ROBOT"), `bekend` ("proficiat agent"), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
