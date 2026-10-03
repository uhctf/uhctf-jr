"""Kleine hulpmiddelen om eenvoudige A4-pdf's te maken met reportlab."""
from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.utils import simpleSplit
from reportlab.pdfgen import canvas

from .paths import ROOT

W, H = A4
MARGE = 2 * cm
LOGO = ROOT / "assets" / "logo.png"

LABELS = {
    "nl": {"begeleiders": "Begeleiders", "antwoord": "Antwoord", "oplossing": "Oplossing", "hints": "Hints"},
    "en": {"begeleiders": "Facilitators", "antwoord": "Answer", "oplossing": "Solution", "hints": "Hints"},
}


class Pdf:
    def __init__(self, pad: Path, titel: str):
        self.c = canvas.Canvas(str(pad), pagesize=A4)
        self.c.setTitle(titel)
        self.c.setAuthor("UHCTF")
        self.y = 0.0
        self._begin(titel)

    def _begin(self, titel: str) -> None:
        c = self.c
        if LOGO.exists():
            c.drawImage(str(LOGO), W - MARGE - 1.8 * cm, H - MARGE - 0.6 * cm, 1.8 * cm, 1.8 * cm,
                        preserveAspectRatio=True, mask="auto")
        c.setFont("Helvetica-Bold", 22)
        c.drawString(MARGE, H - MARGE - 0.4 * cm, titel)
        self.y = H - MARGE - 2 * cm

    def _einde_pagina(self) -> None:
        self.c.setFont("Helvetica", 8)
        self.c.setFillGray(0.5)
        self.c.drawString(MARGE, 1.2 * cm, "UHCTF Jr - uhctf.be - CC BY-NC-SA 4.0")
        self.c.setFillGray(0)
        self.c.showPage()

    def pagina(self, titel: str) -> None:
        self._einde_pagina()
        self._begin(titel)

    def ruimte(self, punten: float) -> None:
        self.y -= punten

    def _regels(self, tekst: str, font: str, grootte: float, indent: float = 0) -> None:
        breedte = W - 2 * MARGE - indent
        for stuk in tekst.split("\n"):
            for regel in simpleSplit(stuk, font, grootte, breedte) or [""]:
                if self.y < MARGE + 1 * cm:
                    self.pagina("")
                self.c.setFont(font, grootte)
                self.c.drawString(MARGE + indent, self.y, regel)
                self.y -= grootte * 1.4

    def kop(self, tekst: str) -> None:
        self.ruimte(6)
        self._regels(tekst, "Helvetica-Bold", 14)
        self.ruimte(2)

    def regel(self, tekst: str, grootte: float = 12, indent: float = 0) -> None:
        self._regels(tekst, "Helvetica", grootte, indent)
        self.ruimte(3)

    def mono(self, tekst: str, grootte: float = 10) -> None:
        # Courier heeft vaste breedte; breek lange regels zelf af zodat niets wegvalt.
        per_regel = int((W - 2 * MARGE) / (grootte * 0.6))
        for stuk in tekst.split("\n"):
            delen = [stuk[i:i + per_regel] for i in range(0, len(stuk), per_regel)] or [""]
            for deel in delen:
                self._regels(deel, "Courier", grootte)
        self.ruimte(3)

    def tabel(self, kop: tuple[str, ...], rijen: list[tuple[str, ...]], breedtes: tuple[float, ...], grootte: float = 10) -> None:
        """Tabel met automatisch afbrekende cellen, \\n in een cel geeft een nieuwe regel. De kop herhaalt na een paginawissel."""
        totaal = sum(breedtes)
        br = [b / totaal * (W - 2 * MARGE) for b in breedtes]

        def teken(cellen: tuple[str, ...], vet: bool) -> None:
            font = "Helvetica-Bold" if vet else "Helvetica"
            regels = []
            for tekst, b in zip(cellen, br):
                lijst: list[str] = []
                for stuk in str(tekst).split("\n"):
                    lijst += simpleSplit(stuk, font, grootte, b - 8) or [""]
                regels.append(lijst)
            hoogte = max(len(r) for r in regels) * grootte * 1.3 + 8
            if self.y - hoogte < MARGE + 1 * cm:
                self.pagina("")
                if not vet:
                    teken(kop, True)
            x, y = MARGE, self.y - hoogte
            for lijst, b in zip(regels, br):
                self.c.setFont(font, grootte)
                if vet:
                    self.c.setFillGray(0.9)
                    self.c.rect(x, y, b, hoogte, fill=1)
                    self.c.setFillGray(0)
                self.c.rect(x, y, b, hoogte)
                for i, regel in enumerate(lijst):
                    self.c.drawString(x + 4, self.y - 4 - grootte * 1.3 * (i + 0.85), regel)
                x += b
            self.y -= hoogte

        teken(kop, True)
        for rij in rijen:
            teken(rij, False)
        self.ruimte(10)

    def opslaan(self) -> None:
        self._einde_pagina()
        self.c.save()


def begeleider(pad: Path, naam: str, antwoord: str | None, oplossing: list[str], hints: list[str],
               taal: str = "nl") -> Pdf:
    """Standaard begeleidersblad. Geeft de (nog niet opgeslagen) Pdf terug zodat er pagina's bij kunnen."""
    t = LABELS.get(taal, LABELS["nl"])
    p = Pdf(pad, f"{naam} - {t['begeleiders']}")
    if antwoord is not None:  # None = uitdaging zonder vlag
        p.kop(t["antwoord"])
        p.c.setFont("Helvetica-Bold", 18)
        p.c.drawString(MARGE, p.y, antwoord)
        p.ruimte(28)
    p.kop(t["oplossing"])
    for regel in oplossing:
        p.regel(regel)
    p.kop(t["hints"])
    for i, h in enumerate(hints, 1):
        p.regel(f"{i}. {h}")
    return p
