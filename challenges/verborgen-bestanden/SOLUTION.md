# Oplossing

1. **notities.txt** begint met de bytes `89 50 4E 47` (`.PNG`): het is een PNG-afbeelding. Open het als afbeelding (of hernoem het naar `notities.png`): er staat `deel 1: magische`.
2. **vakantie.jpg** is een echte foto. Een JPEG eindigt met `FF D9`, maar daarna staat nog tekst: `deel 2: bytes`. Zichtbaar in de hexweergave, als tekst, of met `strings vakantie.jpg`.
3. **boodschappen.txt** is gewoon een boodschappenlijst.

Plak de delen aan elkaar: **magische-bytes**.

Flag: `magische-bytes`
