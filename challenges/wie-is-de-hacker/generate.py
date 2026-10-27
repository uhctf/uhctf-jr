"""Wie is de hacker? Logicapuzzel: schrap verdachten met getuigenverklaringen tot er één overblijft."""
import random
from pathlib import Path

from reportlab.lib.units import cm

from jr.digitaal import schrijf
from jr.pdf import MARGE, W, Pdf, begeleider

NAMEN = ["Lotte", "Yasmine", "Finn", "Arne", "Elise", "Jonas", "Maya", "Lars", "Noor", "Milan", "Emma", "Jules",
         "Lien", "Sam", "Tess", "Ruben", "Fleur", "Bram", "Nina", "Daan", "Fien", "Thomas", "Merel", "Seppe"]

# kenmerk -> (kolomkop, waarden, "ja"-zin, "nee"-zin). In de zinnen komt de waarde op {}.
KENMERKEN = {
    "haar": ("Haar", ["zwart", "bruin", "blond", "rood"], "De hacker heeft {} haar.", "De hacker heeft geen {} haar."),
    "draagt": ("Draagt", ["een bril", "een pet", "een sjaal", "een koptelefoon", "oorbellen"],
               "De hacker draagt {}.", "De hacker draagt geen {}."),
    "apparaat": ("Apparaat", ["een laptop", "een tablet", "een gsm", "een spelconsole"],
                 "De hacker werkte op {}.", "De hacker werkte niet op {}."),
    "schoenen": ("Schoenen", ["rode", "blauwe", "witte", "zwarte"],
                 "De hacker droeg {} schoenen.", "De hacker droeg geen {} schoenen."),
}

TEKST = {
    "titel": "Wie is de hacker?",
    "intro": "Iemand heeft het wachtwoord van de computerklas veranderd! Wie is de hacker? Elke verklaring is waar. Zet bij elke verklaring een kruisje bij wie het niet kan zijn.",
    "verdachten": "De verdachten",
    "verklaringen": "Wat de getuigen zeggen",
    "tip": "Zet bij elke verklaring een kruisje in de kolom van de verdachten die het niet kunnen zijn.",
    "antwoord": "De hacker is:",
    "naam": "Naam",
    "variant": "Variant {i}: {naam}",
    "oplossing": "De hacker is {naam}. Na verklaring {k} blijft enkel {naam} over. Wie viel af bij welke verklaring: {afval}.",
    "afvallers": "{nr}: {namen}",
    "hints": ["Begin met de verklaring die het meeste zegt en schrap wie niet past.",
              "Een zin met 'geen' schrapt wie dat kenmerk wél heeft.",
              "Houd de tabel bij: wie nog geen kruisje heeft, blijft verdacht."],
}


def pas_toe(verdachte: dict, kenmerk: str, waarde: str, ja: bool) -> bool:
    """Is de verklaring waar voor deze verdachte?"""
    return (verdachte[kenmerk] == waarde) == ja


def maak_puzzel(params: dict, taboe: tuple = ()) -> dict:
    n, minimum = params["verdachten"], params["minimum"]
    if not 3 <= n <= 8:
        raise ValueError("verdachten moet tussen 3 en 8 liggen")
    if not 1 <= params["varianten"] <= 3:
        raise ValueError("varianten moet tussen 1 en 3 liggen (er zijn te weinig namen voor meer)")
    if not 2 <= minimum <= n - 1:
        raise ValueError(f"minimum (aantal verklaringen) moet tussen 2 en {n - 1} liggen")
    kenmerken = list(KENMERKEN)
    rng = random.Random(params["seed"])
    for _ in range(500):
        namen = rng.sample([x for x in NAMEN if x not in taboe], n)
        verdachten = [{"naam": naam, **{k: rng.choice(KENMERKEN[k][1]) for k in kenmerken}} for naam in namen]
        if len({tuple(v[k] for k in kenmerken) for v in verdachten}) < n:
            continue  # twee verdachten met dezelfde kenmerken: nooit op te lossen
        hacker = rng.randrange(n)
        over, verklaringen = list(range(n)), []
        while over != [hacker]:
            opties = []
            for k in kenmerken:
                for waarde in KENMERKEN[k][1]:
                    ja = verdachten[hacker][k] == waarde
                    afvallers = [i for i in over if not pas_toe(verdachten[i], k, waarde, ja)]
                    if afvallers:
                        opties.append((len(afvallers), k, waarde, ja, afvallers))
            kleinste = min(o[0] for o in opties)  # liefst kleine stapjes: dan heb je meer verklaringen nodig
            _, k, waarde, ja, afvallers = rng.choice([o for o in opties if o[0] == kleinste])
            over = [i for i in over if i not in afvallers]
            verklaringen.append({"kenmerk": k, "waarde": waarde, "ja": ja, "afvallers": afvallers})
        if len(verklaringen) >= minimum:
            return {"verdachten": verdachten, "hacker": hacker, "verklaringen": verklaringen}
    raise ValueError("Kon geen puzzel maken: verlaag minimum of verhoog het aantal verdachten")


def zin(v: dict) -> str:
    _, _, ja_zin, nee_zin = KENMERKEN[v["kenmerk"]]
    if v["ja"]:
        return ja_zin.format(v["waarde"])
    # "geen een bril" bestaat niet: bij een ontkenning vervalt het lidwoord
    return nee_zin.format(v["waarde"].removeprefix("een ") if "geen {}" in nee_zin else v["waarde"])


def maak_varianten(params: dict) -> list[dict]:
    resultaat, namen = [], ()
    for i in range(params["varianten"]):
        puzzel = maak_puzzel({**params, "seed": params["seed"] + i}, namen)
        namen += tuple(v["naam"] for v in puzzel["verdachten"])
        resultaat.append(puzzel)
    return resultaat


def teken(p: Pdf, puzzel: dict, t: dict, oplossing: bool = False) -> None:
    verdachten, verklaringen = puzzel["verdachten"], puzzel["verklaringen"]
    kenm = list(KENMERKEN)
    kop = (t["naam"], *[KENMERKEN[k][0] for k in kenm], *[str(i + 1) for i in range(len(verklaringen))])
    rijen = []
    for r, v in enumerate(verdachten):
        # in de oplossing staat bij elk afgevallen verdachte een kruisje onder de verklaring waarbij hij afvalt
        kruisen = ["X" if oplossing and r in vk["afvallers"] else "" for vk in verklaringen]
        rijen.append((v["naam"] + ("  <- hacker" if oplossing and r == puzzel["hacker"] else ""),
                      *[v[k] for k in kenm], *kruisen))
    p.kop(t["verdachten"])
    p.tabel(kop, rijen, (3, 1.6, 2.6, 2.6, 1.8, *([0.8] * len(verklaringen))), 10)
    p.kop(t["verklaringen"])
    for i, v in enumerate(verklaringen, 1):
        p.regel(f"{i}. {zin(v)}")


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    puzzels = maak_varianten(params)
    oplossing, antwoorden = [], []
    for i, puzzel in enumerate(puzzels):
        suffix = "" if i == 0 else f"-{i + 1}"  # variant 1 houdt de standaardnaam
        p = Pdf(uit / f"deelnemer{suffix}.pdf", t["titel"])
        p.regel(t["intro"].format(n=params["verdachten"]))
        teken(p, puzzel, t)
        p.ruimte(6)
        p.ruimte(10)
        p.c.setFont("Helvetica-Bold", 14)
        p.c.drawString(MARGE, p.y, t["antwoord"] + " " + "_" * 24)
        p.opslaan()

        naam = puzzel["verdachten"][puzzel["hacker"]]["naam"]
        antwoorden.append(naam.lower())
        afval = "; ".join(t["afvallers"].format(nr=k + 1, namen=", ".join(puzzel["verdachten"][r]["naam"] for r in vk["afvallers"]))
                          for k, vk in enumerate(puzzel["verklaringen"]))
        tekst = t["oplossing"].format(naam=naam, k=len(puzzel["verklaringen"]), afval=afval)
        oplossing.append((t["variant"].format(i=i + 1, naam=naam) + ". " + tekst) if len(puzzels) > 1 else tekst)

    antwoord = antwoorden[0] if len(antwoorden) == 1 else "\n".join(f"variant {i + 1}: {a}" for i, a in enumerate(antwoorden))
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoorden[0] if len(antwoorden) == 1 else None, oplossing, t["hints"], "nl")
    for i, puzzel in enumerate(puzzels, 1):
        b.pagina(f"{t['titel']} - oplossing" + (f" (variant {i})" if len(puzzels) > 1 else ""))
        teken(b, puzzel, t, oplossing=True)
    b.opslaan()
    if params.get("digitaal"):
        for i, puzzel in enumerate(puzzels):
            digitaal(puzzel, uit, "" if i == 0 else f"-{i + 1}", t)
    return antwoord


def digitaal(puzzel: dict, uit: Path, suffix: str, t: dict) -> None:
    """Digitaal potlood: schrap verdachten en vink verklaringen af. De pagina controleert niets en kent de hacker niet."""
    css = """
#verdachten{width:100%;border-collapse:separate;border-spacing:0 6px}
#verdachten th{background:var(--ink);color:#fff;text-align:left;padding:8px 12px;font-family:var(--mono);font-size:13px;text-transform:uppercase;letter-spacing:.06em}
#verdachten th:first-child{}#verdachten th:last-child{}
#verdachten td{background:#fff;padding:9px 12px;border-top:3px solid var(--lijn);border-bottom:3px solid var(--lijn);font-size:17px}
#verdachten td:first-child{border-left:3px solid var(--lijn);font-weight:800}
#verdachten td:last-child{border-right:3px solid var(--lijn);text-align:right}
#verdachten tr:nth-child(odd) td{background:var(--cyaan-zacht)}
#verdachten tr.geschrapt td{background:#ececf2;color:#8a8a99;text-decoration:line-through;text-decoration-thickness:3px;text-decoration-color:var(--magenta)}
#verdachten tr.geschrapt td:last-child{text-decoration:none}
#verdachten button{padding:3px 12px;font-size:14px}
#verklaringen{list-style:none;padding:0;display:grid;gap:10px;margin:0}
.verklaring{width:100%;text-align:left;display:flex;gap:14px;align-items:center;font-weight:600;font-size:18px;padding:12px 14px}
.verklaring::before{content:"";flex:none;width:26px;height:26px;border:3px solid var(--lijn);background:#fff}
.verklaring.gebruikt{background:var(--cyaan-zacht);color:var(--muted);text-decoration:line-through;text-decoration-color:var(--magenta);text-decoration-thickness:2px}
.verklaring.gebruikt::before{background:var(--cyaan) url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M5 13l4 4L19 7' fill='none' stroke='%23222' stroke-width='4' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E") center/80% no-repeat}
"""
    kenm = list(KENMERKEN)
    gegevens = {"kolommen": [t["naam"], *[KENMERKEN[k][0] for k in kenm]],
                "verdachten": [[v["naam"], *[v[k] for k in kenm]] for v in puzzel["verdachten"]],
                "verklaringen": [zin(v) for v in puzzel["verklaringen"]]}
    body = """  <div class="kaart">
    <h2>De verdachten</h2>
    <div style="overflow-x:auto"><table id="verdachten"></table></div>
    <p class="klein" id="over"></p>
    <div class="rij"><button id="wis" type="button">Alles wissen</button></div>
  </div>
  <div class="kaart">
    <h2>Wat de getuigen zeggen</h2>
    <ol id="verklaringen"></ol>
  </div>"""
    schrijf(uit, t["titel"], "Elke verklaring is waar. Schrap de verdachten die het niet kunnen zijn.", body,
            Path(__file__).parent / "digitaal.js", gegevens, t["hints"], css, naam=f"digitaal{suffix}.html")


def check(params: dict) -> None:
    puzzels = maak_varianten({**params, "varianten": 3})
    namen = [v["naam"] for pz in puzzels for v in pz["verdachten"]]
    assert len(set(namen)) == len(namen)  # varianten delen geen verdachten
    for pz in puzzels:
        verdachten, hacker = pz["verdachten"], pz["hacker"]
        assert len(pz["verklaringen"]) >= params["minimum"]
        # alle verklaringen samen laten precies de hacker over; elke verklaring schrapt echt iemand
        over = set(range(len(verdachten)))
        for vk in pz["verklaringen"]:
            assert pas_toe(verdachten[hacker], vk["kenmerk"], vk["waarde"], vk["ja"])  # verklaringen zijn waar
            nieuw = {i for i in over if pas_toe(verdachten[i], vk["kenmerk"], vk["waarde"], vk["ja"])}
            assert nieuw < over
            over = nieuw
        assert over == {hacker}
