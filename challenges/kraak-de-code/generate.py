"""Kraak de code: een recursieve functie waarvan de deelnemers twee uitkomsten moeten berekenen."""
from pathlib import Path

from reportlab.lib.units import cm

from jr.pdf import MARGE, Pdf, begeleider

# naam -> (begin: {x: waarde}, formule in woorden voor de code, python-functie, uitleg)
FUNCTIES = {
    "fibonacci": ({0: 0, 1: 1}, "Code(X - 1) + Code(X - 2)", lambda f, x: f(x - 1) + f(x - 2), "de rij van Fibonacci"),
    "driehoek": ({0: 0}, "Code(X - 1) + X", lambda f, x: f(x - 1) + x, "de driehoeksgetallen (1, 3, 6, 10, ...)"),
    "verdubbel": ({0: 1}, "Code(X - 1) * 2", lambda f, x: f(x - 1) * 2, "de machten van twee"),
}

TEKST = {
    "nl": {
        "titel": "Kraak de code",
        "intro": "Geen mens zal dit ooit oplossen, je hebt zeker een computer nodig om deze code uit te voeren! "
                 "Of toch niet? Reken het uit en plak de twee uitkomsten aan elkaar.",
        "vlag": "Antwoord", "tekst": "Tekst", "functie": "functie", "als": "als", "tabel": "Hulp: vul de tabel verder aan",
        "oplossing": "Code(X) is {uitleg}. Code({a}) = {fa} en Code({b}) = {fb}. Plak ze aan elkaar: {antwoord}.",
        "hints": ["De functie roept zichzelf op.", "Begin klein: reken Code(2), Code(3), Code(4) uit.",
                  "Elke waarde hangt af van de vorige. Maak een tabel."],
    },
    "en": {
        "titel": "Crack the code",
        "intro": "No human will ever solve this, you surely need a computer to run this code! "
                 "Or maybe not? Work it out and glue the two results together.",
        "vlag": "Answer", "tekst": "Text", "functie": "function", "als": "if", "tabel": "Help: continue the table",
        "oplossing": "Code(X) is {uitleg}. Code({a}) = {fa} and Code({b}) = {fb}. Glue them together: {antwoord}.",
        "hints": ["The function calls itself.", "Start small: work out Code(2), Code(3), Code(4).",
                  "Every value depends on the previous one. Make a table."],
    },
}


def waarde(functie: str, x: int) -> int:
    begin, _, stap, _ = FUNCTIES[functie]
    cache: dict[int, int] = dict(begin)

    def f(n: int) -> int:
        if n not in cache:
            cache[n] = stap(f, n)
        return cache[n]
    return f(x)


def antwoord_van(params: dict) -> str:
    if params["functie"] not in FUNCTIES:
        raise ValueError(f"Onbekende functie '{params['functie']}'. Mogelijk: {', '.join(FUNCTIES)}")
    if min(params["a"], params["b"]) < 0 or max(params["a"], params["b"]) > 30:
        raise ValueError("a en b moeten tussen 0 en 30 liggen")
    return f"{waarde(params['functie'], params['a'])}{waarde(params['functie'], params['b'])}"


def generate(params: dict, uit: Path) -> str:
    t = TEKST.get(params["taal"], TEKST["nl"])
    antwoord = antwoord_van(params)
    naam, a, b = params["functie"], params["a"], params["b"]
    begin, formule, _, uitleg = FUNCTIES[naam]

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"])
    code = [f"{t['vlag']} = {t['tekst']}(Code({a})) + {t['tekst']}(Code({b}))", "", f"{t['functie']} Code(X) = {{"]
    code += [f"    {t['als']} X == {x} -> {v}" for x, v in begin.items()]
    code += [f"    -> {formule}", "}"]
    p.mono("\n".join(code), 12)

    if params["hulp"]:
        p.kop(t["tabel"])
        hoogste = max(a, b)
        kolommen = hoogste + 1
        kop = 2.2 * cm  # ruimte voor de rijlabels links
        cel = min(1.4 * cm, (595 - 2 * MARGE - kop) / kolommen)
        for rij, label in enumerate(("X", "Code(X)")):
            y = p.y - 0.9 * cm * (rij + 1)
            p.c.setFont("Helvetica-Bold", 10)
            p.c.drawString(MARGE, y + 0.3 * cm, label)
            for x in range(kolommen):
                p.c.rect(MARGE + kop + x * cel, y, cel, 0.9 * cm)
                p.c.setFont("Helvetica", 10)
                if rij == 0:
                    p.c.drawCentredString(MARGE + kop + x * cel + cel / 2, y + 0.3 * cm, str(x))
                elif x in begin:
                    p.c.drawCentredString(MARGE + kop + x * cel + cel / 2, y + 0.3 * cm, str(begin[x]))
        p.ruimte(2 * cm + 20)
    p.opslaan()

    fa, fb = waarde(naam, a), waarde(naam, b)
    b_pdf = begeleider(uit / "begeleider.pdf", t["titel"], antwoord,
                       [t["oplossing"].format(uitleg=uitleg, a=a, b=b, fa=fa, fb=fb, antwoord=antwoord)],
                       t["hints"], params["taal"])
    b_pdf.mono("X:       " + " ".join(f"{x:>6}" for x in range(max(a, b) + 1)) + "\n"
               "Code(X): " + " ".join(f"{waarde(naam, x):>6}" for x in range(max(a, b) + 1)), 8)
    b_pdf.opslaan()
    return antwoord


def check(params: dict) -> None:
    # Controleer de rekenkunde onafhankelijk met een eenvoudige lus.
    if params["functie"] == "fibonacci":
        x, y = 0, 1
        rij = [x]
        for _ in range(max(params["a"], params["b"])):
            x, y = y, x + y
            rij.append(x)
        assert antwoord_van(params) == f"{rij[params['a']]}{rij[params['b']]}"
    assert antwoord_van(params)
