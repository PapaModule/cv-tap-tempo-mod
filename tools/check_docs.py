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

MU = "[\u00b5\u03bc]"  # µ: znak mikro (U+00B5) lub greckie mu (U+03BC)
OHM = "[\u03a9\u2126]"  # Ω: greckie omega (U+03A9) lub znak oma (U+2126)

FORBIDDEN_ALL = {
    rf"0[.,]1 ?{MU}F": "kondensator HP z v2 (0,1 µF)",
    rf"0[.,]47 ?{MU}F": "0,47 µF odrzucone w v3",
    r"160 ?Hz": "częstotliwość filtra z v2",
    r"τ ?≈ ?1 ?ms": "błędna stała czasowa z v2",
    r"~ ?1 ?ms\b": "impuls ~1 ms z v2 (w v3: 15–135 ms)",
    r"[Zz]ewrzyj tip": "test zwarciem tip-sleeve nie działa (brak zasilania)",
    r"\*{0,2}\bHP\b\*{0,2} ?\(ON/OFF\)": "stara nazwa przełącznika — teraz GATE/TRIG",
    r"\bHP switch": "stara nazwa przełącznika — teraz GATE/TRIG",
    r"[Pp]rzełącznik\w* HP\b": "stara nazwa przełącznika — teraz GATE/TRIG",
    rf"470 ?{OHM}[ ,|*]*1/4 ?W": "R2/R4 muszą być 0,6 W",
    rf"47 ?k{OHM} \(dłuższy": "błędna porada troubleshooting z v2",
}

FORBIDDEN_EXTRA = {
    "schematic.svg": {rf"10 ?k{OHM}": "shunt 10k z v2 (teraz 100k)"},
}

REQUIRED = {
    "README.md": [
        rf"0[.,]22 ?{MU}F", r"BC547B", rf"470 ?{OHM}", r"0,6 ?W", rf"47 ?k{OHM}", rf"100 ?k{OHM}",
        r"GATE/TRIG", r"DO-35", r"DIP-4", r"±10 ?V|20 ?Vpp", r"spec\.md", r"plan\.md",
        r"rezystancj\w* wyjścia",
    ],
    "plan.md": [
        rf"0[.,]22 ?{MU}F", rf"0[.,]33 ?{MU}F", r"BC547B", r"0,6 ?W", rf"47 ?k{OHM}", rf"100 ?k{OHM}",
        r"GATE/TRIG", r"DO-35", r"DIP-4", r"5×7", r"[Mm]inimalny impuls",
        r"[Pp]róg przytrzymania", r"GND_mod", r"GND_ped", r"antyparalel",
        r"\bR7\b", r"\bR8\b", r"[Pp]rąd zwarcia", r"z wtykiem", r"\b[Oo]dłącz zasilanie pedału", r"[Ww]olne miejsce",
    ],
    "schematic.svg": [
        rf"0[.,]22 ?{MU}F", rf"470 ?{OHM}", rf"47 ?k{OHM}", rf"100 ?k{OHM}", r"BC547B",
        r"\bQ1\b", r"\bQ2\b", r"\bD3\b", r"\bD4\b", r"\bOC1\b", r"\bOC2\b",
        r"GATE/TRIG", r"SELECT", r"REC", r"\bR7\b", r"\bR8\b",
    ],
}


def read_checked_text(name: str, path: Path) -> str:
    """Tekst do sprawdzenia. W SVG tylko widoczny tekst (bez komentarzy, z rozwiniętymi encjami)."""
    text = path.read_text(encoding="utf-8")
    if name.endswith(".svg"):
        root = ET.fromstring(text.encode("utf-8"))
        return "\n".join(root.itertext())
    return text


def check(root: Path = ROOT) -> list[str]:
    problems = []
    for name, required in REQUIRED.items():
        path = root / name
        if not path.exists():
            problems.append(f"{name}: brak pliku")
            continue
        try:
            text = read_checked_text(name, path)
        except (OSError, UnicodeDecodeError, ET.ParseError) as err:
            problems.append(f"{name}: błąd odczytu — {err}")
            continue
        forbidden = {**FORBIDDEN_ALL, **FORBIDDEN_EXTRA.get(name, {})}
        for pattern, why in forbidden.items():
            for match in re.finditer(pattern, text):
                line = text.count("\n", 0, match.start()) + 1
                where = f"{name}:{line}" if not name.endswith(".svg") else f"{name}: tekst"
                problems.append(f"{where}: zakazane „{match.group(0)}” — {why}")
        for pattern in required:
            if not re.search(pattern, text):
                problems.append(f"{name}: brak wymaganego wzorca /{pattern}/")
    return problems


if __name__ == "__main__":
    found = check()
    for problem in found:
        print(problem)
    print("OK" if not found else f"\n{len(found)} problem(ów)")
    sys.exit(1 if found else 0)
