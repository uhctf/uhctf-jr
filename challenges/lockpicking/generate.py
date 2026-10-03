"""Lockpicking-station: opdrachtkaart, briefjes met het antwoord voor in de afgesloten doos, en een begeleidersgids."""
from pathlib import Path

from reportlab.lib.units import cm

from jr.pdf import H, MARGE, W, Pdf, begeleider

TEKST = {
    "nl": {
        "titel": "Lockpicking",
        "intro": "Ook sloten kunnen kapot of open gemaakt worden, en wie dat begrijpt, kan ze beter maken. "
                 "Probeer een oefenslot te openen. In de afgesloten doos zit een briefje met het antwoord.",
        "stappen_kop": "Zo werkt het",
        "stappen": [
            "In een slot zitten kleine pennetjes. Met de sleutel staan ze allemaal precies goed.",
            "Zet het spanstuk in het onderste deel van het sleutelgat en draai heel licht, alsof je de sleutel bijna omdraait.",
            "Duw met de pick de pennetjes één voor één omhoog. Voel je een klikje? Dan blijft dat pennetje staan.",
            "Staan alle pennetjes goed? Dan draait het slot open. Haal het briefje uit de doos.",
        ],
        "regels_kop": "Afspraken",
        "regels": ["We oefenen enkel op onze eigen sloten, en nooit op sloten van anderen.",
                   "Breek niets af: werk met gevoel, niet met kracht.",
                   "Schrijf het antwoord van het briefje op en geef het door."],
        "briefje": "Antwoord:",
        "oplossing": "Deelnemers openen het oefenslot met spanstuk en pick. In de afgesloten doos ligt een briefje met het antwoord.",
        "opzet_kop": "Opzet",
        "opzet": ["Per deelnemer of duo: een lockpicking-set (spanstuk + pick) en een oefenslot, bij voorkeur een doorzichtig slot of een eenvoudig hangslot.",
                  "Leg in elke afgesloten doos of elk slot-met-doos één briefje uit briefjes.pdf. Knip ze uit en vouw ze dubbel.",
                  "Zet de doos dicht met het oefenslot. Begin met makkelijke sloten voor de jongsten.",
                  "Houd sloten en sets na het event samen, en tel de pick-sets na.",
                  "Toon eerst de pennetjes (doorzichtig slot of schema) voordat ze zelf proberen."],
        "tips_kop": "Tips voor begeleiders",
        "tips": ["Te veel kracht op het spanstuk is de meest voorkomende fout. Lichtjes!",
                 "Blijft het slot vastzitten, laat even loslaten en opnieuw beginnen.",
                 "Leg uit waarom slotenmakers en beveiligingsonderzoekers dit leren: om sloten beter te maken.",
                 "Gebruik nooit sloten die echt in gebruik zijn."],
        "intro_zonder": "Ook sloten kunnen open gemaakt worden zonder sleutel, en wie dat begrijpt, kan ze beter maken. "
                        "Probeer een oefenslot te openen. Doe dit samen met een begeleider: jij probeert, de begeleider kijkt mee. "
                        "Lukt het? Dan heb je de opdracht gehaald.",
        "oplossing_zonder": "Er is geen vlag. De opdracht is gehaald als de deelnemer het oefenslot opent, onder toezicht van een volwassen begeleider.",
        "opzet_zonder": ["Per deelnemer of duo: een lockpicking-set (spanstuk + pick) en een oefenslot, bij voorkeur een doorzichtig slot of een eenvoudig hangslot.",
                         "Een volwassen begeleider is altijd erbij en kijkt mee. De begeleider geeft uitleg, helpt bij vastlopers en bevestigt dat het gelukt is.",
                         "Begin met makkelijke sloten voor de jongsten.",
                         "Houd sloten en sets na het event samen, en tel de pick-sets na.",
                         "Toon eerst de pennetjes (doorzichtig slot of schema) voordat ze zelf proberen."],
        "regels_zonder": ["We oefenen enkel op onze eigen sloten, en nooit op sloten van anderen.",
                          "Doe dit altijd samen met een begeleider.",
                          "Breek niets af: werk met gevoel, niet met kracht."],
        "stappen_laatste_zonder": "Staan alle pennetjes goed? Dan draait het slot open. Laat het aan je begeleider zien!",
        "hints": ["Duw zachtjes aan het spanstuk, niet te hard.", "Voel je een klikje bij een pennetje? Dan zit het goed.",
                  "Lukt het niet? Laat los en begin opnieuw met minder kracht."],
    },
    "en": {
        "titel": "Lockpicking",
        "intro": "Locks can be opened without the key, and people who understand how can build better locks. "
                 "Try to open a practice lock. Inside the locked box is a note with the answer.",
        "stappen_kop": "How it works",
        "stappen": [
            "A lock contains small pins. With the key they all sit exactly right.",
            "Put the tension wrench in the bottom of the keyhole and turn very lightly, as if you almost turn the key.",
            "Push the pins up one by one with the pick. Do you feel a click? Then that pin stays up.",
            "All pins set? The lock turns open. Take the note out of the box.",
        ],
        "regels_kop": "Rules",
        "regels": ["We only practise on our own locks, never on locks that belong to others.",
                   "Do not break anything: use feel, not force.",
                   "Write down the answer on the note and hand it in."],
        "briefje": "Answer:",
        "oplossing": "Participants open the practice lock with tension wrench and pick. The locked box holds a note with the answer.",
        "opzet_kop": "Setup",
        "opzet": ["Per participant or pair: a lockpicking set (tension wrench + pick) and a practice lock, preferably transparent or a simple padlock.",
                  "Put one note from briefjes.pdf in every locked box. Cut them out and fold them.",
                  "Close the box with the practice lock. Start with easy locks for the youngest.",
                  "Keep locks and sets together after the event, and count the picks.",
                  "Show the pins first (transparent lock or diagram) before they try."],
        "tips_kop": "Tips for facilitators",
        "tips": ["Too much force on the tension wrench is the most common mistake. Light touch!",
                 "If the lock gets stuck, release and start over.",
                 "Explain why locksmiths and security researchers learn this: to make locks better.",
                 "Never use locks that are really in use."],
        "intro_zonder": "Locks can be opened without the key, and people who understand how can build better locks. "
                        "Try to open a practice lock. Do this together with a facilitator: you try, the facilitator watches. "
                        "Did it open? Then you completed the task.",
        "oplossing_zonder": "There is no flag. The task is complete when the participant opens the practice lock, supervised by an adult facilitator.",
        "opzet_zonder": ["Per participant or pair: a lockpicking set (tension wrench + pick) and a practice lock, preferably transparent or a simple padlock.",
                         "An adult facilitator is always present and watches. The facilitator explains, helps when stuck and confirms it worked.",
                         "Start with easy locks for the youngest.",
                         "Keep locks and sets together after the event, and count the picks.",
                         "Show the pins first (transparent lock or diagram) before they try."],
        "regels_zonder": ["We only practise on our own locks, never on locks that belong to others.",
                          "Always do this together with a facilitator.",
                          "Do not break anything: use feel, not force."],
        "stappen_laatste_zonder": "All pins set? The lock turns open. Show it to your facilitator!",
        "hints": ["Use a gentle touch on the tension wrench.", "Feel a click on a pin? Then it is set.",
                  "Stuck? Let go and start over with less force."],
    },
}


def generate(params: dict, uit: Path) -> str | None:
    """Zonder vlag (standaard): enkel opdrachtkaart en begeleidersgids. Met vlag: ook briefjes met het antwoord."""
    t = TEKST.get(params["taal"], TEKST["nl"])
    met_vlag, antwoord, aantal = params["met_vlag"], params["antwoord"], params["briefjes"]
    if met_vlag and aantal < 1:
        raise ValueError("briefjes moet minstens 1 zijn")

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["intro"] if met_vlag else t["intro_zonder"])
    stappen = list(t["stappen"])
    if not met_vlag:
        stappen[-1] = t["stappen_laatste_zonder"]
    regels = t["regels"] if met_vlag else t["regels_zonder"]
    for kop, lijst in ((t["stappen_kop"], stappen), (t["regels_kop"], regels)):
        p.kop(kop)
        for i, regel in enumerate(lijst, 1):
            p.regel(f"{i}. {regel}", 13)
    p.opslaan()

    if met_vlag:
        # Briefjes: 2 kolommen x 4 rijen per pagina, met stippellijnen om uit te knippen.
        b = Pdf(uit / "briefjes.pdf", t["titel"] + " - briefjes")
        kolommen, rijen = 2, 4
        breedte, hoogte = (W - 2 * MARGE) / kolommen, 5 * cm
        c = b.c
        for i in range(aantal):
            if i and i % (kolommen * rijen) == 0:
                b.pagina(t["titel"] + " - briefjes")
            k, r = i % (kolommen * rijen) % kolommen, i % (kolommen * rijen) // kolommen
            x, y = MARGE + k * breedte, b.y - (r + 1) * hoogte
            c.setDash(3, 3)
            c.rect(x, y, breedte, hoogte)
            c.setDash()
            c.setFont("Helvetica", 11)
            c.drawString(x + 0.6 * cm, y + hoogte - 1.2 * cm, t["briefje"])
            c.setFont("Helvetica-Bold", 22)
            c.drawString(x + 0.6 * cm, y + hoogte / 2 - 0.4 * cm, antwoord)
        b.opslaan()

    opzet = t["opzet"] if met_vlag else t["opzet_zonder"]
    g = begeleider(uit / "begeleider.pdf", t["titel"], antwoord if met_vlag else None,
                   [t["oplossing"] if met_vlag else t["oplossing_zonder"]], t["hints"], params["taal"])
    g.kop(t["opzet_kop"])
    for regel in opzet:
        g.regel("- " + regel)
    g.kop(t["tips_kop"])
    for regel in t["tips"]:
        g.regel("- " + regel)
    g.opslaan()
    return antwoord if met_vlag else None


def check(params: dict) -> None:
    if params["met_vlag"]:
        assert params["antwoord"].strip(), "antwoord mag niet leeg zijn"
        assert params["briefjes"] > 0, "briefjes moet groter zijn dan 0"
