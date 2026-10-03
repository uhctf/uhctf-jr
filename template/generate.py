"""Generator voor deze uitdaging.

Contract:
  generate(params, uit) -> str   schrijft het materiaal in map 'uit' en geeft het antwoord terug
  check(params)                  optionele zelftest; gooit een fout als er iets niet klopt
'params' bevat 'antwoord' en alles uit [opties] van challenge.toml (met event-overrides).
"""
from pathlib import Path

from jr.pdf import Pdf, begeleider


def generate(params: dict, uit: Path) -> str:
    antwoord = params["antwoord"]

    p = Pdf(uit / "deelnemer.pdf", "<+Titel+>")
    p.regel("<+Wat de deelnemers krijgen+>")
    p.opslaan()

    b = begeleider(uit / "begeleider.pdf", "<+Titel+>", antwoord,
                   oplossing=["<+Hoe los je het op?+>"],
                   hints=["<+Zachte hint+>", "<+Duidelijkere hint+>"], taal=params["taal"])
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    pass
