"""Hack het portaal: een nep-leerlingenportaal met drie testwoorden achter drie klassieke fouten. Een volgende stap na Webvlaggen: wijzigen in plaats van lezen.

1. klas.html: het gemiddelde zit achter een wazige laag. De tekst staat gewoon in de pagina (Elementen).
2. rapport.html?leerling=24: het nummer in de URL bepaalt wiens rapport je ziet. Leerling 1 is de directeur.
3. beheer.html: de pagina vertrouwt de rol in de sessiesleutel (token, Base64 in Local Storage) en controleert de handtekening niet.

Alles draait in de browser. Het deel dat 'de server' zou moeten controleren, is versleuteld met een sleutel uit de aanvraag (het nummer in de URL, de rol in de
token): wie enkel de broncode leest, vindt de woorden niet; wie de aanvraag wijzigt, wel.
"""
import json
import random
import re
from pathlib import Path

from jr.pdf import Pdf, begeleider
from jr.shared import gebruik

SITE = Path(__file__).parent / "site"

TEKST = {
    "titel": "Hack het portaal",
    "brief": "Opdrachtbrief van {school}. Ons leerlingenportaal staat online en we weten niet hoe veilig het is. Jullie krijgen de toestemming om het te testen, "
             "alleen dit portaal en alleen op deze laptop. We hebben drie testwoorden verstopt op plaatsen waar enkel leraren, de directie of beheerders mogen komen. "
             "Vind ze alle drie: samen vormen ze de zin voor de kluis.",
    "regels": "Afspraken: enkel dit portaal, enkel met toestemming van de school. Dezelfde trucs bij een echte site zonder toestemming zijn strafbaar. "
              "Een echte site controleert dit op de server: hier doet de pagina alsof ze de server is.",
    "tools": "De ontwikkelaarstools open je met F12 of Ctrl+Shift+I. Tabbladen: Elementen (de pagina als boom, aanpasbaar), Netwerk (wat er geladen wordt) en "
             "Toepassing / Application (Chrome en Edge) of Opslag (Firefox): daar staat wat de pagina in je browser bewaart, zoals Local Storage.",
    "oplossing": [
        "Fase 1, Klasgemiddelde (klas.html): onder de wazige laag staat 'Testwoord 1 van 3: {w1}'. Rechtsklik, Inspecteren: de tekst staat gewoon in de pagina. "
        "Verwijder de laag (class laag) en zet de blur uit, of lees de tekst in Elementen.",
        "Fase 2, Mijn rapport (rapport.html?leerling=24): het nummer in de URL bepaalt wiens rapport je ziet. Probeer andere nummers. Leerling 1 is de directeur, met de "
        "notitie 'sleutelwoord 2 is {w2}' en een verwijzing naar beheer.html. Dit is een IDOR (insecure direct object reference).",
        "Fase 3, Beheer (beheer.html): 'Geen toegang, rol leerling'. De pagina kijkt naar de token in Local Storage (sleutel opdracht-portaal-token). "
        "Neem het deel voor de punt, zet het met de Decoder (Base64 naar tekst) om: {{\"gebruiker\":\"sam.peeters\",\"leerling\":24,\"rol\":\"leerling\"}}. "
        "Verander leerling in beheerder, zet terug om naar Base64, plak vervangen deel + de punt + de handtekening terug op dezelfde plek en herlaad de pagina.",
        "Testwoord 3 is '{w3}'. De zin is: {antwoord}.",
        "Bespreking: alles wat in de browser staat, kun je aanpassen. Een server moet bij elke aanvraag controleren wie je bent en wat je mag, en een token moet "
        "een handtekening hebben die de server controleert. Hier staat zelfs het commentaar 'handtekening nog controleren' in de bron.",
    ],
    "hints": [
        "Je bent ingelogd als een gewone leerling. Zoek pagina's waar je niet mag komen en kijk wat de browser eigenlijk al gekregen heeft. Open de ontwikkelaarstools met F12.",
        "Iets wazig of afgedekt? Wat je ziet is niet alles wat de browser kreeg. Kijk in het tabblad Elementen (Inspecteren) en pas de laag aan of lees de tekst.",
        "De URL van je rapport bevat een nummer. Wie zegt dat dit nummer van jou is? Probeer een ander nummer. Wie heeft vast een laag nummer?",
        "De beheerderspagina kijkt naar je sessiesleutel (token). Die staat in de ontwikkelaarstools, bij Toepassing (Chrome, Edge) of Opslag (Firefox), onder Local Storage.",
        "Een token is vaak Base64. Zet het deel voor de punt in de Decoder om naar tekst en kijk bij 'rol'. Verander die, zet het terug om naar Base64 en plak het op dezelfde plaats.",
    ],
}

NAMEN = ["Lena Vermeulen", "Jonas Maes", "Yasmine Aziz", "Bram Wouters", "Noor Janssens", "Milan Peeters", "Emma Dubois", "Arda Yilmaz"]
VAKKEN = ["Nederlands", "Wiskunde", "Wetenschappen", "Frans", "Geschiedenis", "Engels"]


def delen_van(antwoord: str) -> list[str]:
    woorden = [w for w in re.split(r"[-\s]+", antwoord.strip().lower()) if w]
    if len(woorden) < 3 or not all(w.isalnum() and w.isascii() for w in woorden):
        raise ValueError("antwoord moet minstens 3 woorden van letters of cijfers bevatten, gescheiden door koppeltekens, bv. 'vertrouw-nooit-de-browser'")
    return [woorden[0], woorden[1], " ".join(woorden[2:])]  # het laatste deel krijgt de rest


def versleutel(tekst: str, salt: str, sleutel: str) -> str:
    """XOR met salt:sleutel, als hex. Moet gelijk zijn aan ontsleutel() in site/portaal.js."""
    k = f"{salt}:{sleutel}".encode()
    return bytes(b ^ k[i % len(k)] for i, b in enumerate(tekst.encode())).hex()


def ontsleutel(hex_: str, salt: str, sleutel: str) -> str:
    k = f"{salt}:{sleutel}".encode()
    return bytes(b ^ k[i % len(k)] for i, b in enumerate(bytes.fromhex(hex_))).decode()


def maak_rapporten(delen: list[str], rng: random.Random) -> dict[str, dict]:
    def punten():
        return [[v, f"{rng.randint(9, 17)} / 20"] for v in VAKKEN]
    rapporten = {
        "24": {"naam": "Sam Peeters", "klas": "5B", "vakken": punten(), "notitie": ""},
        "1": {"naam": "Mevr. Claes", "klas": "directie", "vakken": [],
              "notitie": f"Interne notitie: sleutelwoord 2 is {delen[1]}. Het beheerderspaneel staat op beheer.html en vraagt een sessiesleutel met de rol beheerder."},
        "2": {"naam": "Dhr. Willems", "klas": "leraar wiskunde", "vakken": [], "notitie": "Personeel: geen rapport."},
        "3": {"naam": "Mevr. Aerts", "klas": "ICT-coördinator", "vakken": [], "notitie": "Personeel: geen rapport."},
    }
    for i, nummer in enumerate((22, 23, 25, 26)):
        rapporten[str(nummer)] = {"naam": NAMEN[(i + rng.randint(0, 3)) % len(NAMEN)], "klas": "5B", "vakken": punten(), "notitie": ""}
    return rapporten


def schrijf_site(uit: Path, params: dict, delen: list[str], hints: list[str]) -> dict:
    rng = random.Random(params["seed"])
    salt = f"portaal-{params['seed']}"
    rapporten = {nr: versleutel(json.dumps(r, ensure_ascii=False), salt, nr) for nr, r in maak_rapporten(delen, rng).items()}
    handtekening = "".join(rng.choice("0123456789abcdef") for _ in range(32))
    geheim3 = versleutel(f"Testwoord 3 van 3: {delen[2]}", salt, "beheerder")
    waarden = {"SCHOOL": params["school"], "SALT": salt, "HANDTEKENING": handtekening, "WOORD1": delen[0], "GEHEIM3": geheim3,
               "RAPPORTEN": json.dumps(rapporten), "HINTS": json.dumps(hints, ensure_ascii=False).replace("</", "<\\/")}
    doel = uit / "site"
    doel.mkdir(parents=True, exist_ok=True)
    for bron in SITE.iterdir():
        tekst = bron.read_text()
        for k, v in waarden.items():
            tekst = tekst.replace("{{" + k + "}}", v)
        assert "{{" not in tekst, f"{bron.name}: onbekende marker"
        (doel / bron.name).write_text(tekst)
    return {"salt": salt, "rapporten": rapporten, "geheim3": geheim3}


def generate(params: dict, uit: Path) -> str:
    t = TEKST
    antwoord = params["antwoord"].strip().lower()
    delen = delen_van(antwoord)
    schrijf_site(uit, params, delen, t["hints"])
    gebruik(uit, params["taal"], "decoder", "spiekbrief")

    p = Pdf(uit / "deelnemer.pdf", t["titel"])
    p.regel(t["brief"].format(school=params["school"]))
    p.regel(t["regels"])
    p.kop("Ontwikkelaarstools")
    p.regel(t["tools"])
    p.opslaan()
    oplossing = [x.format(w1=delen[0], w2=delen[1], w3=delen[2], antwoord=antwoord) for x in t["oplossing"]]
    b = begeleider(uit / "begeleider.pdf", t["titel"], antwoord, oplossing, t["hints"], params["taal"])
    b.opslaan()
    return antwoord


def check(params: dict) -> None:
    """De drie testwoorden zijn terug te vinden langs de bedoelde weg en niet zomaar in de broncode."""
    import tempfile
    antwoord = params["antwoord"].strip().lower()
    delen = delen_van(antwoord)
    with tempfile.TemporaryDirectory() as tmp:
        uit = Path(tmp)
        info = schrijf_site(uit, params, delen, TEKST["hints"])
        alles = {p.name: p.read_text() for p in (uit / "site").iterdir()}
        # fase 1: gewoon in de pagina; fase 2 en 3: niet leesbaar zonder de juiste aanvraag
        assert f"Testwoord 1 van 3: {delen[0]}" in alles["klas.html"]
        tekst = "\n".join(alles.values())
        assert f"sleutelwoord 2 is {delen[1]}" not in tekst and f"Testwoord 3 van 3: {delen[2]}" not in tekst, "testwoord 2 of 3 staat leesbaar in de broncode"
        r1 = json.loads(ontsleutel(info["rapporten"]["1"], info["salt"], "1"))
        assert f"sleutelwoord 2 is {delen[1]}" in r1["notitie"] and "beheer.html" in r1["notitie"]
        assert ontsleutel(info["geheim3"], info["salt"], "beheerder") == f"Testwoord 3 van 3: {delen[2]}"
    assert " ".join(delen).split() == antwoord.replace("-", " ").split()
