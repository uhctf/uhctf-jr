<!-- Dit bestand wordt gegenereerd uit challenge.toml. Pas challenge.toml aan en draai ./jr readme. -->

# Verborgen bestanden

- Author: UHCTF

- Format: booth

- Age: 15–18

- Duration: 20–30 min

- Topic: Digitaal speurwerk (forensics), bestandsformaten, magic bytes

- Materials: de bestanden in `usb/` of de digitale versie op een laptop, het blad met magic bytes (`deelnemer.pdf`)

- Flag Format: het antwoord zelf (hoofdletterongevoelig)

Flag:

<details><summary>TOON</summary><ul><ul>
<li>standaard: <code>magische-bytes</code></li>
</ul></ul></details>

## Beschrijving

Op een USB-stick van een verdachte staan drie onschuldige bestanden: een vakantiefoto, notities en een boodschappenlijst. Of toch niet? De naam van een bestand zegt niet wat erin zit. Kijk naar de bytes zelf.

## Hints

1. De extensie (.txt, .jpg) is maar een naam. De eerste bytes van een bestand verraden het echte formaat: vergelijk ze met de tabel.
2. notities.txt begint niet met tekst. Welk formaat begint met 89 50 4E 47? Open het bestand als dat formaat.
3. Een JPEG eindigt altijd met FF D9. Kijk in de hexweergave of als tekst naar het einde van vakantie.jpg: staat er nog iets na?

## Opzet

De generator maakt drie bestanden in `usb/`: `notities.txt` is in werkelijkheid een PNG-afbeelding met het eerste deel van het antwoord, `vakantie.jpg` is een echte foto met na het einde van de afbeelding (de bytes `FF D9`) nog tekst met het tweede deel, en `boodschappen.txt` is gewoon tekst (een afleider). Het antwoord is beide delen met een koppelteken (hoofdletters en leestekens tellen niet mee in de kluis). Op `deelnemer.pdf` staat een tabel met magic bytes. Met `digitaal = true` komt er een pagina bij met de bestanden en een bestandsinspecteur: een hexweergave, weergave als tekst en weergave als afbeelding. Met eigen gereedschap kan het ook: `file`, `xxd` of `strings` op de map `usb/`.

Na afloop: waarom kijken virusscanners en e-mailfilters naar de inhoud en niet naar de extensie, en hoe verstoppen aanvallers gegevens in onschuldige bestanden?

Dit is een gegenereerde uitdaging. Bouw met de standaardwaarden:

```
./jr build verborgen-bestanden
```

Voor een event met een eigen antwoord:

```
./jr event add <event> verborgen-bestanden --antwoord <woord>
./jr event build <event>
```

De uitvoer bevat minstens `deelnemer.pdf` (uitdelen) en `begeleider.pdf` (antwoord, oplossing, hints).

Opties (standaardwaarde): `taal` ("nl"), `digitaal` (false).

[SOLUTION.md](SOLUTION.md)
