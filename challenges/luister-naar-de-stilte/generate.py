"""Luister naar de stilte: een WAV die bijna stilte lijkt, maar morse bevat. Zichtbaar in het spectrogram, niet te horen.

De WAV wordt met enkel de standaardbibliotheek gemaakt (wave, math, random). check() decodeert het bestand opnieuw met het
een eigen detector (Goertzel per blokje van 10 ms), zodat een bestand waarin de morse niet te lezen is meteen opvalt.
"""
import math
import random
import struct
import wave
from pathlib import Path

from jr import codecs as c
from jr.digitaal import inpakken
from jr.pdf import Pdf, begeleider
from jr.shared import gebruik

SR = 44100          # samplefrequentie: hoog genoeg voor een toon rond 17 kHz
RAMP = 0.006        # seconden om een toon zacht aan en uit te zetten (anders hoor en zie je klikjes)
BROM = 882          # 44100 / 50 Hz: één periode van het netbrom, zo hoeft er niet per sample gesinust te worden

# toon: Hz (vast getal of bereik waaruit de seed kiest), amp: amplitude van de morse (1 = volle schaal),
# ruis: standaardafwijking van de witte ruis, brom: amplitude van het netbrom, lok: (tekst, Hz, amplitude) of None
NIVEAUS = {
    "makkelijk": dict(toon=700, amp=0.30, ruis=0.01, brom=0.0, wpm=10, lok=None),
    "middel": dict(toon=(1100, 1500), amp=0.012, ruis=0.02, brom=0.0, wpm=12, lok=None),
    "moeilijk": dict(toon=(16500, 19500), amp=0.0055, ruis=0.010, brom=0.02, wpm=15, lok=("lokvogel", 1300, 0.03)),
}

TEKST = {
    "titel": "Luister naar de stilte",
    "verhaal": "Een onderzoeker nam in een verlaten radiohut {duur} seconden stilte op. Toch beweert zijn collega dat er een boodschap in zit. "
               "Je hoort bijna niets, maar een geluidsbestand is meer dan wat je hoort.",
    "opdracht_laptop": "Open Luister naar de stilte op de laptop: het geluid staat al in de WAV-decoder. Zoek de boodschap, lees de punten en strepen "
                       "zelf af, zet ze om naar tekst en typ het antwoord in de kluis.",
    "opdracht": "Open wav-decoder/index.html op de computer: het bestand stilte.wav staat al klaar. Zoek de boodschap, lees de punten en strepen "
                "zelf af, zet ze om naar tekst en schrijf het antwoord op.",
    "tip": "Tip: de spiekbrief heeft de morsetabel en de Decoder kan morse omzetten naar tekst.",
    "oplossing": [
        "Het geluid klinkt als zacht gesis. Zet in de WAV-decoder 'Versterken' hoog en open het spectrogram (tijd naar rechts, frequentie naar boven).",
        "Een toon die aan en uit gaat, verschijnt als een rij streepjes en puntjes op een vaste hoogte. Hier: {toon} Hz. Dat is {bereik}.",
        "{lokvogel}",
        "Pas Helderheid en Contrast aan, zoom in en lees de punten en strepen zelf af. Een streep is drie keer zo lang als een punt; een langere pauze scheidt de letters, een nog langere de woorden.",
        "Zet de morse om met de spiekbrief of typ ze in de Decoder (stap Morse naar tekst, letters gescheiden door een spatie, woorden door een /). Het bericht staat {n} keer na elkaar: {bericht}.",
    ],
    "lok_tekst": "Er speelt ook een duidelijkere rij op {lok_toon} Hz: een lokvogel die '{lokvogel}' seint. Die is niet het antwoord.",
    "bereik_laag": "een hoorbare toon",
    "bereik_hoog": "ver boven wat de meeste mensen goed horen: een luidspreker geeft het nauwelijks weer, het spectrogram toont het wel",
    "hints_basis": [
        "Je hoort bijna niets. Maar een geluid kun je ook bekijken: kijk naar de golfvorm en naar het spectrogram.",
        "Zet 'Versterken' hoger en pas helderheid en contrast van het spectrogram aan. De x-as is tijd, de y-as is frequentie. "
        "Zoek een rij streepjes en puntjes die steeds op dezelfde hoogte staat.",
        "Zoom in en lees de korte en lange streepjes af. Een streep is drie keer zo lang als een punt.",
        "Schrijf de punten en strepen op en zet ze om met de morsetabel van de spiekbrief, of met de Decoder (stap Morse naar tekst).",
    ],
    "hint_lok": "Zie je meer dan een rij? Lees ze allemaal af. Niet elk bericht dat je vindt, is het antwoord.",
}


def morse_tekst(antwoord: str) -> list[str]:
    """De woorden die gesein worden. Een koppelteken telt als woordscheiding."""
    woorden = antwoord.upper().replace("-", " ").split()
    for w in woorden:
        for ch in w:
            if ch not in c.MORSE:
                raise ValueError(f"'{ch}' kan niet in morse; gebruik enkel letters, cijfers en koppeltekens")
    if not woorden:
        raise ValueError("het antwoord mag niet leeg zijn")
    return woorden


def intervallen(woorden: list[str], wpm: float, start: float) -> tuple[list[tuple[float, float]], float]:
    """Wanneer staat de toon aan? Geeft [(begin, einde)] in seconden en het eindtijdstip. Punt = 1 eenheid, streep = 3."""
    punt = 1.2 / wpm
    t, rij = start, []
    for wi, woord in enumerate(woorden):
        for ci, letter in enumerate(woord):
            code = c.MORSE[letter]
            for si, teken in enumerate(code):
                d = punt if teken == "." else 3 * punt
                rij.append((t, t + d))
                t += d + (punt if si < len(code) - 1 else 0)
            if ci < len(woord) - 1:
                t += 3 * punt
        if wi < len(woorden) - 1:
            t += 7 * punt
    return rij, t


def kies_toon(profiel: dict, rng: random.Random) -> int:
    toon = profiel["toon"]
    if isinstance(toon, tuple):
        return round(rng.uniform(*toon) / 10) * 10
    return toon


def render(antwoord: str, niveau: str, seed: int, herhalingen: int) -> tuple[list[float], dict]:
    """Maak de samples (floats tussen -1 en 1) en de gegevens van het bestand."""
    if niveau not in NIVEAUS:
        raise ValueError(f"niveau moet {', '.join(NIVEAUS)} zijn, kreeg '{niveau}'")
    profiel = NIVEAUS[niveau]
    rng = random.Random(seed)
    woorden = morse_tekst(antwoord)
    toon = kies_toon(profiel, rng)

    echt, t = [], 2.5  # eerst 2,5 s stilte
    for i in range(herhalingen):
        rij, t = intervallen(woorden, profiel["wpm"], t)
        echt += rij
        t += 3.0 if i < herhalingen - 1 else 0
    duur = t + 2.0

    lok_rij = []
    if profiel["lok"]:  # de lokvogel herhaalt zich over de hele opname, rustiger dan het echte bericht
        lok_woorden = morse_tekst(profiel["lok"][0])
        tl = 1.0
        while tl < duur - 4:
            rij, tl = intervallen(lok_woorden, 10, tl)
            lok_rij += rij
            tl += 2.5

    n = int(duur * SR)
    ruis = profiel["ruis"]
    samples = [rng.gauss(0.0, ruis) for _ in range(n)]
    if profiel["brom"]:
        bromtabel = [profiel["brom"] * (math.sin(2 * math.pi * i / BROM) + 0.5 * math.sin(4 * math.pi * i / BROM)) for i in range(BROM)]
        for i in range(n):
            samples[i] += bromtabel[i % BROM]

    def zet_toon(rij, hz, amp):
        w = 2 * math.pi * hz / SR
        rs = int(RAMP * SR)
        for begin, einde in rij:
            a, b = int(begin * SR), min(int(einde * SR), n)
            for i in range(a, b):
                x = min(i - a, b - i, rs) / rs  # 0..1 aan de randen, daartussen 1
                samples[i] += amp * (0.5 - 0.5 * math.cos(math.pi * x)) * math.sin(w * i)

    zet_toon(echt, toon, profiel["amp"])
    if profiel["lok"]:
        zet_toon(lok_rij, profiel["lok"][1], profiel["lok"][2])
    return samples, {"toon": toon, "wpm": profiel["wpm"], "duur": duur, "woorden": woorden, "niveau": niveau,
                     "herhalingen": herhalingen, "lok": profiel["lok"]}


def schrijf_wav(pad: Path, samples: list[float]) -> None:
    ints = [max(-32768, min(32767, round(s * 32767))) for s in samples]
    with wave.open(str(pad), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(struct.pack(f"<{len(ints)}h", *ints))


def lees_wav(pad: Path) -> list[float]:
    with wave.open(str(pad), "rb") as w:
        assert w.getnchannels() == 1 and w.getsampwidth() == 2 and w.getframerate() == SR
        ruw = w.readframes(w.getnframes())
    return [x / 32768 for x in struct.unpack(f"<{len(ruw) // 2}h", ruw)]


def goertzel(samples: list[float], begin: int, lengte: int, hz: float) -> float:
    k = hz * lengte / SR
    coef = 2 * math.cos(2 * math.pi * k / lengte)
    s1 = s2 = 0.0
    for x in samples[begin:begin + lengte]:
        s1, s2 = x + coef * s1 - s2, s1
    return s1 * s1 + s2 * s2 - coef * s1 * s2


def schoon(aan: list[bool], kort: int = 3) -> list[bool]:
    """Ruispieken wegfilteren: een gat korter dan 'kort' blokjes midden in een puls en een puls korter dan 'kort' blokjes tellen niet."""
    def runs_van(x):
        r, i = [], 0
        while i < len(x):
            j = i
            while j < len(x) and x[j] == x[i]:
                j += 1
            r.append((i, j, x[i]))
            i = j
        return r
    aan = list(aan)
    for waarde in (False, True):  # eerst korte gaten dichten, dan korte pulsen wissen
        for i, j, w in runs_van(aan):
            if w == waarde and j - i < kort and (waarde is False and 0 < i and j < len(aan) or waarde is True):
                aan[i:j] = [not waarde] * (j - i)
    return aan


def decodeer(samples: list[float], hz: float) -> str:
    """Zelftest: vermogen per blokje van 10 ms (gemeten over 20 ms), drempel halverwege (in dB), dan lengtes van pulsen en pauzes.
    De deelnemers doen dit zelf met hun ogen in het spectrogram; de WAV-decoder rekent dit niet voor hen uit."""
    blok = SR // 100
    nb = len(samples) // blok
    # elk blokje meet over 20 ms (dat blokje en het volgende): meer signaal tegenover de ruis, tijdresolutie van 10 ms
    db = [10 * math.log10(goertzel(samples, b * blok, min(2 * blok, len(samples) - b * blok), hz) + 1e-20) for b in range(nb)]
    gesorteerd = sorted(db)
    laag, hoog = gesorteerd[int(0.05 * nb)], gesorteerd[int(0.98 * nb)]
    for _ in range(12):  # 2-means op de niveaus in dB: het gemiddelde van 'uit' en van 'aan', de drempel ligt ertussen
        a = [d for d in db if abs(d - laag) <= abs(d - hoog)]
        b = [d for d in db if abs(d - laag) > abs(d - hoog)]
        laag, hoog = sum(a) / len(a), sum(b) / len(b)
    drempel = (laag + hoog) / 2
    aan = [d >= drempel for d in db]
    aan = schoon(aan)
    runs, i = [], 0
    while i < nb:
        j = i
        while j < nb and aan[j] == aan[i]:
            j += 1
        runs.append((aan[i], j - i))
        i = j
    pulsen = [lengte for a, lengte in runs if a]
    assert pulsen, "geen pulsen gevonden"
    c1, c2 = min(pulsen), max(pulsen)  # 2-means op de lengtes: korte pulsen (punten) en lange (strepen)
    for _ in range(12):
        k = [p for p in pulsen if abs(p - c1) <= abs(p - c2)]
        l = [p for p in pulsen if abs(p - c1) > abs(p - c2)]
        c1, c2 = sum(k) / len(k), (sum(l) / len(l) if l else c2)
    punt = c1 if c2 / c1 >= 1.8 else min(pulsen)
    uit = []
    for i, (a, lengte) in enumerate(runs):
        if a:
            uit.append("." if lengte < 2 * punt else "-")
        elif 0 < i < len(runs) - 1:  # de stilte voor de eerste en na de laatste puls telt niet
            uit.append("" if lengte < 2 * punt else (" " if lengte < 5 * punt else " / "))
    code = "".join(uit).strip()
    return " ".join("".join(c.MORSE_OMGEKEERD.get(x, "?") for x in w.split()) for w in code.split(" / ")).lower()


def bouw_wav(params: dict, pad: Path) -> dict:
    samples, info = render(params["antwoord"], params["niveau"], params["seed"], params["herhalingen"])
    schrijf_wav(pad, samples)
    return info


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    antwoord = params["antwoord"].strip().lower()
    wav = uit / "stilte.wav"
    info = bouw_wav({**params, "antwoord": antwoord}, wav)
    gebruik(uit, params["taal"], "wav-decoder", "decoder", "spiekbrief", opties={"wav-decoder": {"geluid": str(wav)}})

    hints = list(t["hints_basis"])
    if info["lok"]:
        hints.insert(2, t["hint_lok"])
    if params.get("digitaal"):  # de WAV-decoder met het geluid ingebouwd is de digitale versie; de hints komen eronder
        (uit / "digitaal.html").write_text(inpakken((uit / "wav-decoder" / "index.html").read_text(), hints))

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["verhaal"].format(duur=round(info["duur"])))
    p.regel(t["opdracht_laptop" if params.get("digitaal") else "opdracht"])
    p.regel(t["tip"])
    p.opslaan()

    hoog = info["toon"] > 5000
    lok = t["lok_tekst"].format(lok_toon=info["lok"][1], lokvogel=info["lok"][0]) if info["lok"] else "Er speelt geen tweede rij."
    oplossing = [x.format(toon=info["toon"], bereik=t["bereik_hoog" if hoog else "bereik_laag"], lokvogel=lok, n=info["herhalingen"],
                          bericht=" ".join(info["woorden"]).lower()) for x in t["oplossing"]]
    oplossing.append(f"Niveau: {info['niveau']}, {info['wpm']} woorden per minuut. De WAV-decoder (golfvorm en spectrogram) zit in wav-decoder/ en in de digitale pagina.")
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, oplossing, hints, params["taal"])
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    """Maak de WAV en decodeer hem opnieuw: zowel het echte bericht als (als die er is) de lokvogel moeten terugkomen."""
    import tempfile
    antwoord = params["antwoord"].strip().lower()
    with tempfile.TemporaryDirectory() as tmp:
        pad = Path(tmp) / "stilte.wav"
        info = bouw_wav({**params, "antwoord": antwoord}, pad)
        samples = lees_wav(pad)
    verwacht = " ".join(w.lower() for w in info["woorden"] * info["herhalingen"])
    gekregen = decodeer(samples, info["toon"])
    assert gekregen == verwacht, f"decoderen gaf '{gekregen}' in plaats van '{verwacht}'"
    if info["lok"]:
        lok = decodeer(samples, info["lok"][1])
        assert lok.startswith(info["lok"][0]), f"de lokvogel gaf '{lok}'"
