import argparse
import os
import shutil
import sys
from pathlib import Path

from . import event as ev
from . import readme, scaffold, shared, venv
from .challenge import Challenge, alle
from .paths import ROOT, TEMPLATE, ToolError


def parse_sets(items: list[str] | None, antwoord: str | None = None) -> dict:
    overrides = {}
    if antwoord is not None:
        overrides["antwoord"] = antwoord
    for item in items or []:
        if "=" not in item:
            raise ToolError(f"--set verwacht sleutel=waarde, kreeg '{item}'")
        k, v = item.split("=", 1)
        overrides[k.strip()] = v
    return overrides


def cmd_setup(a):
    venv.setup()


def cmd_list(a):
    kop = f"{'uitdaging':24} {'type':10} {'standaardantwoord':24} extra vereisten"
    # Vet in een terminal; gewone tekst bij doorsturen naar een bestand of als NO_COLOR gezet is.
    vet = sys.stdout.isatty() and "NO_COLOR" not in os.environ
    print(f"\033[1m{kop}\033[0m" if vet else kop)
    for naam in alle():
        ch = Challenge(naam)
        if ch.zonder_vlag:
            antw = "(geen vlag)"
        else:
            antw = ch.standaard_antwoord or ("(berekend)" if not ch.is_static else "-")
        extra = "ja" if venv.has_requirements(ch.requirements) else "-"
        print(f"{naam:24} {ch.type:10} {antw:24} {extra}")


def cmd_install(a):
    namen = alle() if a.alles else [a.uitdaging]
    if not namen or namen == [None]:
        raise ToolError("Geef een uitdaging op, of gebruik --alles")
    for naam in namen:
        ch = Challenge(naam)
        if venv.has_requirements(ch.requirements):
            print(f"{naam}: vereisten installeren ...")
            venv.pip_install(ch.requirements)
        else:
            print(f"{naam}: geen extra vereisten")


def cmd_readme(a):
    if a.check:
        oud = readme.verouderd()
        if oud:
            raise ToolError("Verouderd (draai ./jr readme): " + ", ".join(str(p.relative_to(ROOT)) for p in oud))
        print("README's zijn up-to-date")
        return
    gewijzigd = readme.schrijf()
    for p in gewijzigd:
        print(f"geschreven: {p.relative_to(ROOT)}")
    if not gewijzigd:
        print("Niets te doen: alles is al up-to-date")


def cmd_new(a):
    doel = scaffold.nieuwe_uitdaging(a.uitdaging, "static" if a.statisch else "generated")
    readme.schrijf([a.uitdaging])
    print(f"Aangemaakt: {doel.relative_to(ROOT)}")
    print("Volgende stappen: vul challenge.toml en SOLUTION.md in, daarna ./jr readme" +
          ("; plaats materiaal in src/." if a.statisch else "; werk generate.py bij."))


def cmd_build(a):
    venv.ensure_venv()
    ch = Challenge(a.uitdaging)
    overrides = parse_sets(a.set, a.antwoord)
    if a.uit:
        uit = Path(a.uit)
        if uit.exists() and any(uit.iterdir()):
            raise ToolError(f"{uit} is niet leeg. Kies een lege map, zodat er geen oude bestanden blijven staan.")
    else:
        uit = ROOT / "out" / ch.naam
        shutil.rmtree(uit, ignore_errors=True)  # standaardmap: altijd vers beginnen
    antwoord = ch.build(uit, overrides)
    print(f"Gebouwd in {uit}")
    if antwoord is not None:
        print(f"Antwoord: {antwoord}")


def cmd_check(a):
    venv.ensure_venv()
    namen = alle() if a.alles else [a.uitdaging]
    if not namen or namen == [None]:
        raise ToolError("Geef een uitdaging op, of gebruik --alles")
    mislukt = 0
    for naam in namen:
        try:
            print(f"{naam}: {Challenge(naam).check()}")
        except (ToolError, AssertionError, Exception) as e:  # een mislukte test mag de rest niet stoppen
            mislukt += 1
            print(f"{naam}: MISLUKT - {e}")
    if a.alles:
        for naam in shared.alle():
            try:
                print(f"gedeeld/{naam}: {shared.Resource(naam).check()}")
            except (ToolError, AssertionError, Exception) as e:
                mislukt += 1
                print(f"gedeeld/{naam}: MISLUKT - {e}")
        oud = readme.verouderd()
        if oud:
            mislukt += 1
            print("README's verouderd (draai ./jr readme): " + ", ".join(str(p.relative_to(ROOT)) for p in oud))
    if mislukt:
        raise ToolError(f"{mislukt} controle(s) mislukt")


def cmd_shared(a):
    if a.actie == "list":
        print(f"{'gedeelde bron':20} type")
        for naam in shared.alle():
            print(f"{naam:20} {shared.Resource(naam).type}")
        return
    if not a.naam:
        raise ToolError(f"./jr shared {a.actie} <naam>")
    r = shared.Resource(a.naam)
    if a.actie == "build":
        venv.ensure_venv()
        uit = Path(a.uit) if a.uit else ROOT / "out" / "gedeeld" / r.naam
        if uit.exists() and any(uit.iterdir()):
            raise ToolError(f"{uit} is niet leeg. Kies een lege map.")
        r.build(uit, parse_sets(a.set))
        print(f"Gebouwd in {uit}")
    elif a.actie == "check":
        venv.ensure_venv()
        print(f"{r.naam}: {r.check()}")


def cmd_event(a):
    if a.actie == "new":
        doel = ev.nieuw(a.event, TEMPLATE / "EVENT.md")
        print(f"Aangemaakt: {doel.relative_to(ROOT)}")
        return
    e = ev.Event(a.event)
    if a.actie == "add":
        overrides = e.add(a.uitdaging, parse_sets(a.set, a.antwoord))
        print(f"{a.uitdaging} toegevoegd aan {a.event}" + (f" met {overrides}" if overrides else " (standaardwaarden)"))
    elif a.actie == "remove":
        e.remove(a.uitdaging)
        print(f"{a.uitdaging} verwijderd uit {a.event}")
    elif a.actie == "show":
        for ch, overrides in e.uitdagingen():
            print(f"{ch.naam:24} {ch.type:10} {overrides or ''}")
    elif a.actie == "install":
        for ch, _ in e.uitdagingen():
            if venv.has_requirements(ch.requirements):
                print(f"{ch.naam}: vereisten installeren ...")
                venv.pip_install(ch.requirements)
    elif a.actie == "build":
        venv.ensure_venv()
        uit = e.build()
        print(f"Klaar: {uit.relative_to(ROOT)} (antwoorden: ANTWOORDEN.pdf)")


def main(argv=None):
    p = argparse.ArgumentParser(prog="jr", description="UHCTF Jr tooling")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("setup", help="maak .venv en installeer de algemene vereisten").set_defaults(f=cmd_setup)
    sub.add_parser("list", help="toon alle uitdagingen").set_defaults(f=cmd_list)

    s = sub.add_parser("install", help="installeer de vereisten van een uitdaging")
    s.add_argument("uitdaging", nargs="?")
    s.add_argument("--alles", action="store_true")
    s.set_defaults(f=cmd_install)

    s = sub.add_parser("new", help="maak een nieuwe uitdaging")
    s.add_argument("uitdaging")
    s.add_argument("--statisch", action="store_true", help="statische uitdaging (standaard: gegenereerd)")
    s.set_defaults(f=cmd_new)

    s = sub.add_parser("readme", help="genereer de README's uit challenge.toml")
    s.add_argument("--check", action="store_true", help="faal als een README niet up-to-date is")
    s.set_defaults(f=cmd_readme)

    s = sub.add_parser("build", help="bouw een uitdaging")
    s.add_argument("uitdaging")
    s.add_argument("--antwoord", help="ander antwoord dan de standaard")
    s.add_argument("--set", action="append", metavar="SLEUTEL=WAARDE", help="optie overschrijven (herhaalbaar)")
    s.add_argument("--uit", help="uitvoermap (standaard: out/<uitdaging>)")
    s.set_defaults(f=cmd_build)

    s = sub.add_parser("check", help="bouw met standaardwaarden en voer de zelftest uit")
    s.add_argument("uitdaging", nargs="?")
    s.add_argument("--alles", action="store_true")
    s.set_defaults(f=cmd_check)

    s = sub.add_parser("shared", help="gedeeld materiaal (decoder, spiekbrief, ...)")
    s.add_argument("actie", choices=["list", "build", "check"])
    s.add_argument("naam", nargs="?")
    s.add_argument("--set", action="append", metavar="SLEUTEL=WAARDE")
    s.add_argument("--uit")
    s.set_defaults(f=cmd_shared)

    s = sub.add_parser("event", help="beheer events")
    s.add_argument("actie", choices=["new", "add", "remove", "show", "install", "build"])
    s.add_argument("event")
    s.add_argument("uitdaging", nargs="?")
    s.add_argument("--antwoord")
    s.add_argument("--set", action="append", metavar="SLEUTEL=WAARDE")
    s.set_defaults(f=cmd_event)

    a = p.parse_args(argv)
    try:
        if a.cmd == "event" and a.actie in ("add", "remove") and not a.uitdaging:
            raise ToolError(f"./jr event {a.actie} <event> <uitdaging>")
        a.f(a)
    except ToolError as e:
        print(f"Fout: {e}", file=sys.stderr)
        return 1
    return 0
