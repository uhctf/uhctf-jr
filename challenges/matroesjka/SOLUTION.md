# Oplossing

`vakantiefoto.png` is een gewone foto met een zip-bestand erachter geplakt. Een fotoviewer stopt aan het einde van de afbeelding en toont gewoon de foto. Een zip-programma zoekt de inhoudstafel aan het einde van het bestand en vindt zo het verstopte bestand.

- Windows: kopieer het bestand naar het bureaublad, zet bestandsextensies aan in Verkenner, hernoem `vakantiefoto.png` naar `vakantiefoto.zip` en open het. Of: rechtsklik > 7-Zip > Archief openen (zonder hernoemen).
- macOS of Linux: `unzip vakantiefoto.png`.
- Oudere deelnemers: `file vakantiefoto.png` ziet enkel een PNG, maar `binwalk vakantiefoto.png` toont ook de zip erachter.

In de zip zit `geheim.txt`: "Gevonden! Het antwoord is: **verstoppertje**".

Flag: `verstoppertje`

Met `lagen = 2` of meer zit er in de zip eerst weer een foto (`vakantiefoto-2.png`, ...) met een zip erachter. Herhaal tot je `geheim.txt` vindt.
