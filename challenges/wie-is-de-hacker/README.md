<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Wie is de hacker?

- Author: UHCTF

- Format: booth

- Age: 8–12

- Duration: 10 min

- Topic: Logisch redeneren, deductie

- Materials: geprinte puzzel (`deelnemer.pdf`), potlood

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>jonas</code></li>
</ul></ul></details>

## Beschrijving

Iemand heeft het wachtwoord van de computerklas veranderd! Er zijn een paar verdachten, en de getuigen weten elk een stukje van het verhaal. Combineer wat ze zeggen en schrap de verdachten één voor één. Wie is de hacker?

## Hints

1. Begin met de verklaring die het meeste zegt en schrap wie niet past.
2. Een zin met 'geen' schrapt wie dat kenmerk wél heeft.
3. Houd de tabel bij: wie nog geen kruisje heeft, blijft verdacht.

## Opzet

Print `deelnemer.pdf` per kind of team en geef potloden mee. Op het blad staat een tabel met de verdachten en hun kenmerken, en een lijst verklaringen van getuigen. Per verklaring zetten de kinderen een kruisje in de kolom van elke verdachte die het niet kan zijn; wie overblijft, is de hacker. Elke verklaring is waar voor de hacker, maar geen enkele is op zichzelf genoeg. Het antwoord is de naam van de hacker, in kleine letters.

Met `verdachten` en `minimum` bepaal je de moeilijkheid: meer verdachten en meer verklaringen is moeilijker. Met `varianten = 3` krijg je drie puzzels met andere verdachten en een andere hacker (`deelnemer.pdf`, `deelnemer-2.pdf`, `deelnemer-3.pdf`), zodat een volgend groepje het antwoord niet kan doorvertellen. `begeleider.pdf` toont per puzzel de ingevulde tabel. Met `digitaal = true` komt er per variant ook een klikbare versie bij voor op een laptop (`digitaal.html`, `digitaal-2.html`, ...): een digitaal potlood waarmee de kinderen verdachten schrappen en verklaringen afvinken. De pagina controleert niets en kent de hacker niet. Dezelfde `seed` geeft altijd dezelfde puzzel; elke puzzel heeft precies één oplossing.

Na afloop kun je bespreken hoe echte onderzoekers sporen combineren: één aanwijzing is nooit genoeg, samen vertellen ze het verhaal.

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build wie-is-de-hacker
```

Voor een event met andere opties:

```
./jr event add <event> wie-is-de-hacker --set optie=waarde
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `seed` (2025), `verdachten` (6), `minimum` (5), `varianten` (1), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
