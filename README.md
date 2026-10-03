<p align="center"><img src="assets/logo.png" alt="UHCTF logo" width="200"></p>

# UHCTF Jr

*English: see [README.en.md](README.en.md).*

Materiaal voor de outreach- en junior-evenementen van [UHCTF](https://uhctf.be).
We maken security toegankelijk en leuk voor kinderen en jongeren, met digitale en fysieke uitdagingen.

## Structuur

- [challenges/](challenges/): herbruikbare uitdagingen. Eén map per uitdaging, met een README en een SOLUTION.
- [events/](events/): een specifiek evenement in een bepaald formaat. Een event kiest uitdagingen uit `challenges/` en beschrijft planning, materiaal en score.

| Event | Doelgroep |
| --- | --- |
| [Dag van de Wetenschap](events/dag-van-de-wetenschap/) | families, kinderen en jongeren |
| [Workshop voor jongvolwassenen](events/workshop-jongvolwassenen/) | jongvolwassenen |
| [Tienerdemo](events/tienerdemo/) | tieners |

## Uitgangspunten

- Nederlands is de hoofdtaal. Sommige uitdagingen of evenementen zijn beschikbaar in meerdere talen (bv., Nederlands `README.md` en Engels `README.en.md`).
- Weinig voorkennis nodig. Liefst werkt alles offline in de browser of op papier.
- Flags kunnen simpelweg het antwoord op de uitdaging of een raadsel zijn. Het `uhctf{...}` formaat kan ook gebruikt worden.

## Licentie

- Uitdagingen, documentatie en afdrukbaar materiaal: [CC BY-NC-SA 4.0](LICENSE-CONTENT)
- Code: [MIT](LICENSE)
- Commercieel gebruik? Neem contact op via [uhctf.be](https://uhctf.be).

## Aan de slag

```
./jr setup                          # eenmalig: virtuele omgeving en vereisten
./jr list                           # alle uitdagingen
./jr build doolhof                  # bouw een uitdaging met het standaardantwoord
./jr event add mijn-event doolhof --antwoord kangoeroe
./jr event build mijn-event         # pdf's + antwoordenlijst in events/mijn-event/out/
```

Gegenereerde uitdagingen hebben altijd een standaardantwoord, maar elk event kan een eigen antwoord kiezen. Statische uitdagingen hebben vast materiaal.

## Bijdragen

Zie [CONTRIBUTING.md](CONTRIBUTING.md).

