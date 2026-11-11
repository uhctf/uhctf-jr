# Oplossing

Het bericht `SBKF OBWB KXRX` bestaat uit drie woorden, en elk woord is met een andere verschuiving versleuteld (Caesar). Verschuif de letters van elk woord terug (of ROT-N vooruit, met N de verschuiving van dat woord):

1. `SBKF` is 3 posities verschoven (ROT-3): S→V, B→E, K→N, F→I. Dat is **VENI**.
2. `OBWB` is 7 posities verschoven (ROT-7): O→V, B→I, W→D, B→I. Dat is **VIDI**.
3. `KXRX` is 11 posities verschoven (ROT-11): K→V, X→I, R→C, X→I. Dat is **VICI**.

Antwoord: **VENI VIDI VICI** (de beroemde woorden van Caesar: "ik kwam, ik zag, ik overwon").

Flag: `veni vidi vici` (spaties tellen niet mee in de kluis)

De verschuivingen staan in `challenge.toml` onder `verschuivingen`: één per woord, allemaal verschillend. Het caesarwiel op de laptop helpt: stel een verschuiving in, tik een woord in en kijk of er een echt woord uitkomt. Daarna volgt het volgende woord met een nieuwe verschuiving.
