"""Gedeelde coderingen (binair, hex, base64, ROT-N, morse, XOR), gebruikt door de generatoren en de spiekbrief.

Elke functie werkt op tekst. 'naar_*' pakt in, 'van_*' pakt uit.
"""
import base64

MORSE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.", "G": "--.", "H": "....", "I": "..",
    "J": ".---", "K": "-.-", "L": ".-..", "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-", "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-", "5": ".....", "6": "-....", "7": "--...",
    "8": "---..", "9": "----.", "-": "-....-",
}
MORSE_OMGEKEERD = {v: k for k, v in MORSE.items()}


def naar_binair(s: str) -> str:
    return " ".join(f"{b:08b}" for b in s.encode())


def van_binair(s: str) -> str:
    return bytes(int(x, 2) for x in s.split()).decode()


def naar_hex(s: str) -> str:
    return s.encode().hex()


def van_hex(s: str) -> str:
    return bytes.fromhex(s).decode()


def naar_base64(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def van_base64(s: str) -> str:
    return base64.b64decode(s).decode()


def rot(s: str, n: int) -> str:
    """Caesar/ROT-N: verschuif letters n plaatsen vooruit in het alfabet; andere tekens blijven."""
    def stap(ch: str) -> str:
        if "A" <= ch <= "Z":
            return chr((ord(ch) - 65 + n) % 26 + 65)
        if "a" <= ch <= "z":
            return chr((ord(ch) - 97 + n) % 26 + 97)
        return ch
    return "".join(stap(c) for c in s)


def naar_morse(s: str) -> str:
    return " ".join(MORSE[c] for c in s.upper())


def van_morse(s: str) -> str:
    return "".join(MORSE_OMGEKEERD[c] for c in s.split()).lower()


def xor_naar_hex(s: str, sleutel: str) -> str:
    data, sl = s.encode(), sleutel.encode()
    return bytes(b ^ sl[i % len(sl)] for i, b in enumerate(data)).hex()


def xor_van_hex(hex_: str, sleutel: str) -> str:
    data, sl = bytes.fromhex(hex_), sleutel.encode()
    return bytes(b ^ sl[i % len(sl)] for i, b in enumerate(data)).decode()
