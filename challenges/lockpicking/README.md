<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Lockpicking

- Author: UHCTF

- Format: booth

- Age: 12–18

- Duration: 10–20 min

- Topic: Hoe sloten werken, ethiek van beveiligingsonderzoek

- Materials: lockpicking-sets (spanstuk + pick), oefensloten (bij voorkeur doorzichtig of een eenvoudig hangslot); in de variant met vlag ook een afsluitbare doos per slot en geprinte briefjes (`briefjes.pdf`)

- Flag Format: geen vlag; de opdracht zelf is de actie

## Beschrijving

Ook sloten kunnen open gemaakt worden zonder sleutel, en wie begrijpt hoe, kan ze beter maken. Deelnemers proberen een oefenslot te openen met een lockpicking-set, samen met een volwassen begeleider die meekijkt. Het openen van het slot is de opdracht: er is geen vlag.

Er is ook een variant mét vlag: dan zit in een afgesloten doos een briefje met het antwoord (zie Opzet).

## Hints

1. Duw zachtjes aan het spanstuk, niet te hard.
2. Voel je een klikje bij een pennetje? Dan zit het goed.
3. Lukt het niet? Laat los en begin opnieuw met minder kracht.

## Opzet

Er zijn twee vormen:

1. **Zonder vlag (standaard).** De deelnemer opent een oefenslot onder toezicht van een volwassen begeleider, die uitleg geeft en bevestigt dat het gelukt is. Er is niets in te leveren.
2. **Met vlag.** Zet `met_vlag = true` in het event (`./jr event add <event> lockpicking --set met_vlag=ja --antwoord <woord>`). Dan bevat `briefjes.pdf` briefjes met het antwoord (standaard `dietrich`, optie `briefjes`, 8 per pagina) om uit te knippen en in een afgesloten doos te leggen. Wie de doos opent, vindt het antwoord.

`deelnemer.pdf` is de opdrachtkaart voor aan de tafel en `begeleider.pdf` heeft de opzet en tips. Het `antwoord` wordt enkel gebruikt in de variant met vlag.

Veiligheid: enkel oefenen op eigen sloten, nooit op sloten van anderen, en altijd onder toezicht van een volwassene. Tel de sets na afloop na.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build lockpicking
```

Voor een event met een eigen antwoord:

```
./jr event add <event> lockpicking --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `met_vlag` (false), `briefjes` (8).

[SOLUTION.md](SOLUTION.md)
