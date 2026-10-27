<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Phishing of echt?

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 10 min

- Topic: Phishing herkennen, veilig omgaan met berichten

- Materials: geprinte kaartjes (`deelnemer.pdf`), potlood

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>vissen</code></li>
</ul></ul></details>

## Beschrijving

Je krijgt elke dag berichten: van vrienden, van familie, van spelletjes. Maar soms probeert iemand je te beetnemen om je wachtwoord of gegevens te stelen. Dat heet phishing. Welke berichten zijn nep? Zoek de rode vlaggen.

## Hints

1. Kijk eerst naar de afzender: ken je die?
2. Vraagt het bericht je wachtwoord of gegevens, of is er haast? Dan is het nep.
3. Een link met rare tekens of spelfouten in de naam is een rode vlag.

## Opzet

Print `deelnemer.pdf` per kind of team en geef potloden mee. Op het blad staan berichtenkaartjes (sms, e-mail, chat, pop-up), elk met een nummer en een letter. Een deel is nep, de rest is echt. De kinderen zoeken de rode vlaggen (onbekende afzender, haast of dreigen, te mooi om waar te zijn, vraagt wachtwoord of gegevens, rare link of spelling), zetten een kruisje bij elk nepbericht en schrijven de letters van de nepberichten op, in de volgorde van de nummers. Dat spelt het antwoord. `begeleider.pdf` toont per kaartje of het echt of nep is, welke rode vlaggen erin zitten en waarom een echt bericht in orde is.

Het aantal nepberichten is het aantal letters van het antwoord (3 tot 8); `echt` bepaalt hoeveel echte berichten ertussen staan (1 tot 5). Zet je meerdere woorden in `antwoord`, gescheiden door een komma, dan krijg je een variant per woord (`deelnemer.pdf`, `deelnemer-2.pdf`, `deelnemer-3.pdf`) met andere kaartjes en een ander antwoord, zodat een volgend groepje het niet kan doorvertellen.

Met `digitaal = true` komt er per variant ook een versie bij voor op een laptop (`digitaal.html`, `digitaal-2.html`, ...): de kinderen vinken per bericht de rode vlaggen aan en markeren de berichten die ze nep vinden; onderaan staan de letters van die berichten. De pagina controleert niets. De uitleg per bericht staat alleen in `begeleider.pdf`.

Bespreek na afloop: wat doe je als je een nepbericht krijgt? Niet klikken, niets invullen, en het aan een volwassene tonen. De berichten in de generator zijn verzonnen voor 10 à 11 jaar; je vindt ze in `generate.py`.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build phishing-of-echt
```

Voor een event met een eigen antwoord:

```
./jr event add <event> phishing-of-echt --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (2025), `echt` (2), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
