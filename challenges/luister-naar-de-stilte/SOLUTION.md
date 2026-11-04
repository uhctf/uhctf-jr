# Oplossing: Luister naar de stilte

Standaardantwoord: `radiostilte` (de seed kiest de exacte frequentie; zie `begeleider.pdf` van de bouw).

1. Open de WAV-decoder (de digitale pagina). De kop toont 44 100 Hz, mono, 16 bit, ongeveer 25 s. Afspelen klinkt als zacht gesis en de golfvorm lijkt een vlakke lijn.
2. Zet **Versterken** hoog: in de golfvorm verschijnt een rij streepjes en puntjes. Dat is de **lokvogel** (1300 Hz) en hij seint `lokvogel`. Dat is niet het antwoord.
3. Het spectrogram (tijd naar rechts, frequentie naar boven) toont twee horizontale rijen: een op ongeveer 1,3 kHz (de lokvogel) en een zwakkere helemaal bovenaan, rond 17 kHz. Pas Helderheid en Contrast aan als de bovenste lijn nauwelijks zichtbaar is.
4. Pas Helderheid en Contrast aan, zoom in (Inzoomen of het muiswiel) en lees de punten en strepen van de bovenste rij zelf af. Een streep is drie keer zo lang als een punt, een pauze van drie punten scheidt de letters en een van zeven de woorden.
5. Zet de morse om met de morsetabel van de spiekbrief of in de Decoder (stap Morse naar tekst, letters gescheiden door een spatie en woorden door een `/`): `radiostilte`. Het bericht klinkt twee keer na elkaar.

Wie de golfvorm enkel versterkt en de lokvogel decodeert, typt `lokvogel`: dat opent geen slot. Dat is bedoeld.

## Variaties

- `niveau = "middel"`: een toon van ongeveer 1200 Hz, zacht onder ruis, geen lokvogel.
- `niveau = "makkelijk"`: een hoorbare piep van 700 Hz.
- Vanaf de opdrachtregel: `./jr build luister-naar-de-stilte --set niveau=middel`.
