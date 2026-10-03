# Oplossing

De QR-code is donkerblauw op zwart en staat "negatief" (de code is lichter dan de achtergrond). In de [beeldbewerker](../_gedeeld/beeldbewerker/):

- zet het blauwe kanaal op 1000% en zet Inverteren op 100%, of
- verhoog de belichting (+5) en zet Grijstinten en Inverteren op 100%.

Scan daarna de code van het scherm met een telefoon: het antwoord staat erin. Standaard is dat **night-vision**.

`./jr check robot-qr` controleert (met `zbarimg`, indien aanwezig) dat de QR-code leesbaar is.
