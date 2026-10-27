# TALim-workshop Techniek & IT (security)

- Doelgroep: leerlingen 3e graad lagere school (5e leerjaar, 10–11 jaar)
- Formaat: workshop in kleine groepjes (6 à 8 leerlingen)
- Duur: 30 minuten per workshop, 2 à 3 keer na elkaar met een ander groepje

Het thema is Techniek & IT, met een workshop rond security. De focus ligt op doe-activiteiten.

## Verloop van een sessie (30 minuten)

Een groepje van 6 à 8 leerlingen verdeel je in teams van 2 à 3. Elk team krijgt een eigen laptop en een pakket opdrachten op papier. Doolhof, woordzoeker en lockpicking blijven op papier (of fysiek). De andere opdrachten bestaan op papier en op de laptop: dezelfde puzzel met hetzelfde antwoord, dus een team kan beide proberen of per opdracht kiezen. De digitale versies zijn hulpmiddelen, zoals de decoder: ze controleren niets. Het team bepaalt zelf wanneer het klaar is en typt het antwoord in de kluis. Ze lossen zoveel mogelijk op binnen de tijd, in de volgorde die ze zelf kiezen. Er zijn bewust meer opdrachten dan tijd.

| Wanneer | Wat |
| --- | --- |
| 0–5 min | welkom, korte uitleg over security en de kluis, teamnaam invullen op de laptop |
| 5–28 min | de teams werken zelfstandig; begeleiders lopen rond met hints en controleren de mastermind-gokken |
| 28–30 min | kluis open? Diploma's printen en bespreken: wat leerden we over wachtwoorden en phishing? |

Elk antwoord typen de teams in **de kluis** op de laptop. Met 3 goede antwoorden gaat de kluis open en kunnen ze hun diploma printen. Elk extra antwoord opent een extra slot, dus snelle teams blijven bezig.

Het pakket per team. Behalve doolhof en woordzoeker bestaan alle opdrachten op papier en op de laptop, met dezelfde puzzel en hetzelfde antwoord:

| Opdracht | Op papier | Op de laptop |
| --- | --- | --- |
| [Romeinse geheimen](../../challenges/romeinse-geheimen/) | bericht en alfabetstrook, de decoder om te controleren | een caesarwiel dat je draait |
| [Laag na laag](../../challenges/laag-na-laag/) | het bericht geprint | het bericht om te kopiëren, de lagen pak je uit met de decoder. Dat sluit aan op het Caesarcijfer van Romeinse geheimen (de decoder heeft ook een ROT-stap) |
| [Doolhof](../../challenges/doolhof/) | potlood op het doolhof | alleen op papier |
| [Wie is de hacker?](../../challenges/wie-is-de-hacker/) | schrappen in een tabel | verdachten schrappen en verklaringen afvinken |
| [Phishing of echt?](../../challenges/phishing-of-echt/) | berichtenkaartjes aankruisen | rode vlaggen aanvinken en berichten als nep markeren |
| [Wachtwoord-mastermind](../../challenges/wachtwoord-mastermind/) | een begeleider controleert de gokken | de pagina geeft de feedback per vak, zoals de begeleider |

Voor teams die eerder klaar zijn:

- [Woordzoeker](../../challenges/woordzoeker/): een snelle extra puzzel, alleen op papier.
- [Lockpicking](../../challenges/lockpicking/): een vaste hoek op een aparte tafel met een volwassene erbij, zonder vlag. Het telt niet mee voor de kluis.

Je hebt zoveel laptops nodig als teams (3 à 4).

## Uitdagingen

De uitdagingen en antwoorden staan in [event.toml](event.toml). Bouw alles met `./jr event build talim-workshop`.

| Uitdaging | Leeftijd | Rol |
| --- | --- | --- |
| [Romeinse geheimen](../../challenges/romeinse-geheimen/) | 8–12 | pakket |
| [Laag na laag](../../challenges/laag-na-laag/) | 12–15 | pakket. De uitdaging is gemarkeerd 12–15; hier met de decoder en hints op de laptop |
| [Doolhof](../../challenges/doolhof/) | 8–12 | pakket |
| [Wie is de hacker?](../../challenges/wie-is-de-hacker/) | 8–12 | pakket |
| [Phishing of echt?](../../challenges/phishing-of-echt/) | 8–12 | pakket |
| [Wachtwoord-mastermind](../../challenges/wachtwoord-mastermind/) | 8–12 | pakket |
| [Woordzoeker](../../challenges/woordzoeker/) | 8–12 | extra |
| [Lockpicking](../../challenges/lockpicking/) | 12–18 | extra, 1-op-1 met een volwassene. De uitdaging is gemarkeerd 12–18 |

## De laptopmap

`./jr event build talim-workshop` maakt naast de pdf's ook `events/talim-workshop/out/laptop/`. Die map bevat alles om zonder internet of server te werken:

- `index.html`: de startpagina met teamnaam, een kaart per digitale opdracht en de hulpmiddelen.
- een map per opdracht met `index.html`: de digitale versie. Die komt er alleen als `digitaal = true` staat bij die opdracht in [event.toml](event.toml).
- `kluis/index.html`: de kluis. Een goed antwoord van een willekeurige opdracht opent een slot (elke opdracht telt één keer, op papier of digitaal). De antwoorden staan enkel als hash in de pagina. Met 3 sloten open verschijnt een diploma met de teamnaam om af te drukken. De knop "Nieuw team (begeleider)" wist alles voor het volgende team.
- `decoder/index.html`: de decoder, in het Nederlands.

Elke pagina heeft bovenaan een link terug naar de startpagina en het UHCTF-logo. De pagina's zijn licht en gebruiken de kleuren van het logo.

### Digitaal aan of uit

Zet in [event.toml](event.toml) `digitaal = true` of `digitaal = false` bij elke opdracht. Bij `false` (of als de sleutel ontbreekt) is er alleen het papieren materiaal en staat de opdracht niet op de startpagina. De antwoorden en de kluis veranderen niet. Lockpicking heeft geen digitale versie.

De instellingen van de laptopmap (titel, aantal sloten en introtekst) staan in de tabel `[laptop]` bovenaan [event.toml](event.toml).

## Voorbereiding

1. Bouw alles één keer: `./jr event build talim-workshop`. Print alles uit dezelfde bouw. Mastermind en Wie is de hacker? hebben vaste seeds, zodat een herbouw hetzelfde geeft.
2. Kopieer de map `out/laptop/` (bv. met een USB-stick) naar elke laptop. Open `index.html` in Chrome of Firefox en maak er een bladwijzer van. Er is geen internet nodig.
3. Test de kluis één keer met een paar antwoorden uit `ANTWOORDEN.pdf` en druk daarna op "Nieuw team".
4. Maak per team een pakket: één blad van elke opdracht (bij mastermind ook `profiel.pdf`).
5. Speel het voorbeeld op het mastermind-blad (grijze rij) hardop voor als een team die opdracht start.

## Materiaal

- per team: een laptop met de laptopmap, en het pakket op papier (zie hierboven). Bij mastermind hoort ook het profielblad (`profiel.pdf`).
- optioneel de `spiekbrief` uit `romeinse-geheimen/` of `laag-na-laag/` als spiekbrief bij de decoder
- `ANTWOORDEN.pdf` en de `begeleider.pdf`'s voor de begeleiders
- een printer bij de hand voor de diploma's (of laat de begeleider ze achteraf afdrukken)
- potloden, per team een paar extra
- lockpicking-sets en oefensloten, bij voorkeur doorzichtige. Het aantal sets bepaalt hoeveel koppels tegelijk bezig zijn.

## Score

Geen score. Het gaat om doen en ervaren.

## Opzet en tips

- Alle teams hebben dezelfde puzzels en dezelfde antwoorden. Teams kunnen antwoorden dus doorgeven: laat ze niet naast elkaar zitten, en vraag ze het voor zich te houden.
- Hou lockpicking altijd onder toezicht van een volwassene. Toon eerst hoe de pennetjes in een slot werken, voordat de kinderen zelf proberen.
