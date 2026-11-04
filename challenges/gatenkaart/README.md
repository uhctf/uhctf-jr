<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Gatenkaart

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 10–15 min

- Topic: Cardan-rooster, steganografie, sleutels

- Materials: boekbladzijden (`deelnemer.pdf`), kartonnen kaarten met gaten (`kaarten.pdf`), karton, lijm, hobbymes

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>tussen de regels</code></li>
</ul></ul></details>

## Beschrijving

Dit boek lijkt heel gewoon, maar er zit een geheime zin in verstopt. Je krijgt een paar kartonnen kaarten met gaten. Elke kaart past op precies één bladzijde. Leg de kaart op de juiste bladzijde en lees de letters door de gaten.

## Hints

1. Probeer een kaart op elke bladzijde. Op de meeste bladzijden zie je onzin.
2. Lees de gaten zoals je een boek leest: rij per rij, van links naar rechts.
3. Elke kaart geeft één woord. Zet ze in de volgorde van de kaartnummers.

## Opzet

Dit is een Cardan-rooster: een eeuwenoude manier om een geheim bericht in een gewone tekst te verstoppen. De kaart is de sleutel; zonder kaart is het boek gewoon tekst.

`deelnemer.pdf` bevat de uitleg en de bladzijden van het boek. `kaarten.pdf` heeft één kaart per woord van het antwoord. Print alles op **ware grootte** (niet "passend maken"), anders vallen de gaten niet op de letters. Plak de kaarten op karton en snij de grijze vakjes uit met een hobbymes; snij daarna de kaart uit langs de stippellijn. De rand van de kaart valt dan precies op het kader van de bladzijde. Test elke kaart op zijn bladzijde voor het event; `begeleider.pdf` toont per kaart de juiste bladzijde met de gaten gemarkeerd.

De generator kiest zo veel mogelijk letters die al in de tekst staan, zodat de bladzijden er gewoon uitzien. Hij controleert ook dat een kaart op een verkeerde bladzijde geen woord van de zin geeft. Met minder `kolommen` en `rijen` worden de gaten groter en makkelijker te snijden. Een andere `seed` geeft andere bladzijden en kaarten.

Variant: geef één kaart en één bladzijde voor jongere kinderen (antwoord van één woord, `paginas = 3`).

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build gatenkaart
```

Voor een event met een eigen antwoord:

```
./jr event add <event> gatenkaart --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (1), `paginas` (6), `kolommen` (28), `rijen` (24).

[SOLUTION.md](SOLUTION.md)
