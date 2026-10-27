<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Wachtwoord-mastermind

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 10 min

- Topic: Veilige wachtwoorden, logisch redeneren

- Materials: geprint profiel (`profiel.pdf`) en gokkenlijst (`deelnemer.pdf`), 1 van elk per team van 2 à 3; potlood, liefst ook kleurpotloden; de begeleider controleert de gokken

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>(willekeurig, elke bouw een ander profiel)</code></li>
</ul></ul></details>

## Beschrijving

Veel mensen maken een wachtwoord van dingen die iedereen op hun profiel kan lezen. Kun jij het wachtwoord raden?

Het wachtwoord bestaat uit een paar dingen van het profiel, in een bepaalde volgorde. Doe een gok en de begeleider zegt per vak of het juist is, fout, of juist maar op de verkeerde plaats. Net als bij Mastermind, maar met profielgegevens in plaats van kleuren.

## Hints

1. Alle delen van het wachtwoord staan in het profiel.
2. Begin met een gok en gebruik de feedback: wat staat goed, wat niet?
3. Een letter die fout is, zit niet in het wachtwoord. Die kun je uitsluiten.

## Opzet

Print per team (2 à 3 kinderen) `profiel.pdf` (het profiel van het verzonnen kind) en `deelnemer.pdf` (de gokkenlijst, met bovenaan een uitgewerkt voorbeeld). Met `varianten = 3` bouw je drie verschillende profielen met elk een eigen wachtwoord (`profiel.pdf`, `profiel-2.pdf`, `profiel-3.pdf`, met bijpassende `deelnemer`-bladen): geef aan teams die naast elkaar zitten of na elkaar komen een ander profiel, zodat ze het antwoord niet kunnen doorvertellen. De begeleider heeft `begeleider.pdf` met het juiste wachtwoord en controleert elke gok per letter: juist, fout of juist maar op de verkeerde plaats. De kinderen markeren dat zelf in het vak: vinkje, kruisje of pijltje, of ze kleuren het in. Een blad heeft 6 gokken (optie `pogingen`); met logisch redeneren lukt het meestal in 3 à 5.

Loop het voorbeeld op het blad eerst samen door; lukt het nog niet, speel dan een gok hardop mee. Bespreek na afloop waarom een wachtwoord dat uit je profiel te halen is, niet veilig is. Standaard (`seed = 0`) krijg je bij elke bouw een willekeurig profiel en wachtwoord: print dan alle bladen en `ANTWOORDEN.pdf` uit dezelfde bouw. Voor een event zet je best een vaste `seed`; die geeft altijd hetzelfde profiel (variant i gebruikt `seed + i - 1`). De gebruikte seed staat in `begeleider.pdf`.

Met `digitaal = true` komt er per variant ook een spelbare versie bij voor op een laptop (`digitaal.html`, `digitaal-2.html`, ...): de kinderen kiezen items uit het profiel en de pagina geeft per vak de feedback (juist, fout of verkeerde plaats), zoals de begeleider op papier. De pagina zegt nooit of het wachtwoord gevonden is; dat zien de kinderen zelf. Onderaan staat de tekst van hun gok om in de kluis te typen.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build wachtwoord-mastermind
```

Voor een event met andere opties:

```
./jr event add <event> wachtwoord-mastermind --set optie=waarde
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (0), `lengte` (4), `aantal` (8), `varianten` (1), `pogingen` (6), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
