#!/usr/bin/env python3
"""Sprawdza, czy README.md, plan.md i schematic.svg są zgodne ze spec.md v3.

Wykrywa pozostałości po v2 (zakazane wzorce) i brak kluczowych wartości v3
(wymagane wzorce). Kierunków diod w SVG nie sprawdza — to kontrola wizualna.
Użycie: python3 tools/check_docs.py   (kod wyjścia 0 = OK)
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FORBIDDEN_ALL = {
    r"0[.,]1 ?µF": "kondensator HP z v2 (0,1 µF)",
    r"0[.,]47 ?µF": "0,47 µF odrzucone w v3",
    r"160 ?Hz": "częstotliwość filtra z v2",
    r"τ ?≈ ?1 ?ms": "błędna stała czasowa z v2",
    r"zewrzyj tip": "test zwarciem tip-sleeve nie działa (brak zasilania)",
    r"HP \(ON/OFF\)": "stara nazwa przełącznika — teraz GATE/TRIG",
    r"470 ?Ω, 1/4 ?W": "R2/R4 muszą być 0,6 W",
    r"47 ?kΩ \(dłuższy": "błędna porada troubleshooting z v2",
}

FORBIDDEN_EXTRA = {
    "schematic.svg": {r"10 ?kΩ": "shunt 10k z v2 (teraz 100k)"},
}

REQUIRED = {
    "README.md": [
        r"0[.,]22 ?µF", r"BC547B", r"470 ?Ω", r"0,6 ?W", r"47 ?kΩ", r"100 ?kΩ",
        r"GATE/TRIG", r"DO-35", r"DIP-4", r"±10 ?V|20 ?Vpp", r"spec\.md", r"plan\.md",
    ],
    "plan.md": [
        r"0[.,]22 ?µF", r"0[.,]33 ?µF", r"BC547B", r"0,6 ?W", r"47 ?kΩ", r"100 ?kΩ",
        r"GATE/TRIG", r"DO-35", r"DIP-4", r"5×7", r"[Mm]inimalny impuls",
        r"[Pp]róg przytrzymania", r"GND_mod", r"GND_ped", r"antyparalel",
    ],
    "schematic.svg": [
        r"0[.,]22 ?µF", r"470 ?Ω", r"47 ?kΩ", r"100 ?kΩ", r"BC547B",
        r"\bQ1\b", r"\bQ2\b", r"\bD3\b", r"\bD4\b", r"\bOC1\b", r"\bOC2\b",
        r"GATE/TRIG", r"SELECT", r"REC",
    ],
}


def check() -> list[str]:
    problems = []
    for name, required in REQUIRED.items():
        path = ROOT / name
        if not path.exists():
            problems.append(f"{name}: brak pliku")
            continue
        text = path.read_text(encoding="utf-8")
        forbidden = {**FORBIDDEN_ALL, **FORBIDDEN_EXTRA.get(name, {})}
        for pattern, why in forbidden.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                problems.append(f"{name}:{line}: zakazane „{match.group(0)}” — {why}")
        for pattern in required:
            if not re.search(pattern, text):
                problems.append(f"{name}: brak wymaganego wzorca /{pattern}/")
        if name.endswith(".svg"):
            try:
                ET.fromstring(text.encode("utf-8"))
            except ET.ParseError as err:
                problems.append(f"{name}: niepoprawny XML — {err}")
    return problems


if __name__ == "__main__":
    found = check()
    for problem in found:
        print(problem)
    print("OK" if not found else f"\n{len(found)} problem(ów)")
    sys.exit(1 if found else 0)
