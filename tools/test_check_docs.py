"""Testy tools/check_docs.py. Uruchomienie: python3 -m unittest tools/test_check_docs.py"""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import check_docs  # noqa: E402

CLEAN_README = (
    "0.22µF BC547B 470Ω 0,6 W 47kΩ 100kΩ GATE/TRIG DO-35 DIP-4 ±10V "
    "spec.md plan.md filtr HP SW_HP impuls ~15–135 ms\n"
)
CLEAN_PLAN = (
    "0.22µF 0.33µF BC547B 0,6 W 47kΩ 100kΩ GATE/TRIG DO-35 DIP-4 5×7 "
    "Minimalny impuls Próg przytrzymania GND_mod GND_ped antyparalel "
    "rezystor 1kΩ i 10kΩ do testów R7 R8\n"
)
CLEAN_SVG = (
    '<?xml version="1.0" encoding="UTF-8"?><svg xmlns="http://www.w3.org/2000/svg">'
    "<text>0.22µF 470Ω 47kΩ 100kΩ BC547B Q1 Q2 D3 D4 OC1 OC2 GATE/TRIG SELECT REC R7 R8</text>"
    "</svg>\n"
)


class CheckDocsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("README.md", CLEAN_README)
        self.write("plan.md", CLEAN_PLAN)
        self.write("schematic.svg", CLEAN_SVG)

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, name, text):
        (self.root / name).write_text(text, encoding="utf-8")

    def problems(self):
        return check_docs.check(self.root)

    def assert_flagged(self, name, fragment):
        hits = [p for p in self.problems() if p.startswith(name) and fragment in p]
        self.assertTrue(hits, f"oczekiwano zgłoszenia „{fragment}” w {name}, jest: {self.problems()}")

    def test_clean_docs_pass(self):
        self.assertEqual(self.problems(), [])

    def test_hp_bold_markdown_flagged(self):
        self.write("README.md", CLEAN_README + "| **HP** (ON/OFF) | Filtr |\n")
        self.assert_flagged("README.md", "HP")

    def test_hp_switch_phrase_flagged(self):
        self.write("plan.md", CLEAN_PLAN + "Zmontuj HP switch.\nPrzełącznik HP podłącz.\n")
        hp = [p for p in self.problems() if p.startswith("plan.md") and "HP" in p]
        self.assertEqual(len(hp), 2, self.problems())

    def test_unreadable_file_reported_with_file_prefix(self):
        (self.root / "plan.md").write_bytes(b"0.22\xb5F \xff\xfe")
        self.assert_flagged("plan.md", "błąd odczytu")

    def test_greek_mu_and_ohm_sign_flagged(self):
        self.write("README.md", CLEAN_README + "C 0.1μF, R 470Ω, 1/4W\n")
        self.assert_flagged("README.md", "0.1μF")
        self.assert_flagged("README.md", "1/4W")

    def test_quarter_watt_470_in_table_cells_flagged(self):
        self.write("plan.md", CLEAN_PLAN + "| Rezystor | 470Ω | 1/4W |\n")
        self.assert_flagged("plan.md", "1/4W")

    def test_capitalised_tip_short_flagged(self):
        self.write("plan.md", CLEAN_PLAN + "Zewrzyj tip jacka do sleeve.\n")
        self.assert_flagged("plan.md", "ewrzyj tip")

    def test_v2_one_ms_pulse_flagged_but_v3_range_allowed(self):
        self.write("README.md", CLEAN_README + "gate skracany do ~1ms\n")
        self.assert_flagged("README.md", "~1ms")
        self.write("README.md", CLEAN_README)
        self.assertEqual(self.problems(), [])

    def test_svg_label_only_in_comment_is_missing(self):
        self.write("schematic.svg", CLEAN_SVG.replace(" Q2 ", " ").replace("</svg>", "<!-- Q2 --></svg>"))
        self.assert_flagged("schematic.svg", "Q2")

    def test_input_pulldown_required_in_svg_and_plan(self):
        self.write("schematic.svg", CLEAN_SVG.replace(" R7 R8", ""))
        self.write("plan.md", CLEAN_PLAN.replace(" R7 R8", ""))
        self.assert_flagged("schematic.svg", "R7")
        self.assert_flagged("plan.md", "R8")

    def test_svg_forbidden_value_as_entity_flagged(self):
        self.write("schematic.svg", CLEAN_SVG.replace("</svg>", "<text>0.1&#181;F</text></svg>"))
        self.assert_flagged("schematic.svg", "0.1µF")


if __name__ == "__main__":
    unittest.main()
