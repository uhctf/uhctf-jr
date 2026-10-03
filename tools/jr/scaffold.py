from .challenge import CHALLENGES, NAAM_RE
from .paths import TEMPLATE, ToolError


def nieuwe_uitdaging(naam: str, type_: str):
    if not NAAM_RE.match(naam):
        raise ToolError("Naam moet uit kleine letters, cijfers en koppeltekens bestaan (bv. mijn-uitdaging)")
    doel = CHALLENGES / naam
    if doel.exists():
        raise ToolError(f"Uitdaging '{naam}' bestaat al")
    doel.mkdir(parents=True)
    titel = naam.replace("-", " ").capitalize()
    (doel / "SOLUTION.md").write_text("# Oplossing\n\n<+Uitleg+>\n")
    if type_ == "generated":
        (doel / "challenge.toml").write_text((TEMPLATE / "challenge.generated.toml").read_text().replace("<+Naam+>", titel))
        (doel / "generate.py").write_text((TEMPLATE / "generate.py").read_text())
    else:
        (doel / "challenge.toml").write_text((TEMPLATE / "challenge.static.toml").read_text().replace("<+Naam+>", titel))
        (doel / "src").mkdir()
        (doel / "src" / ".gitkeep").write_text("")
    return doel
