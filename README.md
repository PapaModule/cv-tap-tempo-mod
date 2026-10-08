# CV Tap Tempo Mod — EHX SMMH + Cathedral

Modyfikacja sprzętowa dodająca wejścia CV trigger/gate z Eurorack do funkcji tap tempo w pedałach:

- **EHX Stereo Memory Man with Hazarai** (delay)
- **EHX Cathedral** (reverb)

Wersja układu: **v3 (2026-10-08)**. Projekt oparty na modyfikacji [navs.modular.lab](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html).

> Budujesz? Zacznij od [plan.md](plan.md) — instrukcja krok po kroku z pomiarami i punktami przerwy. Wartości i połączenia: [spec.md](spec.md).

---

## Co robi ten mod

Każdy pedał otrzymuje trzy wejścia CV 3.5mm (Eurorack, gate/trigger 5–10V, odporne na sygnały ±10V / 20 Vpp):

| Wejście | Opis |
|---|---|
| **A** | Trigger/gate, wybierane przez SELECT |
| **B** | Trigger/gate, wybierane przez SELECT |
| **C** | Zawsze aktywne, zawsze TRIG |

Oraz trzy przełączniki:

| Przełącznik | Funkcja |
|---|---|
| **SELECT** (ON/OFF/ON) | Wybór aktywnego wejścia: A / wyłączone / B |
| **GATE/TRIG** (ON/OFF) | Tor A/B. **GATE:** tap trwa tyle co gate (długi gate = przytrzymanie). **TRIG:** każdy gate = jedno krótkie tapnięcie (15–133 ms) |
| **REC** (ON/OFF) | Ręczne przytrzymanie tap — SMMH: nagrywanie pętli, Cathedral: infinite reverb |

Przytrzymanie tapu: SMMH — od 0,5 s nagrywa pętlę; Cathedral — od ~350 ms włącza infinite reverb. W trybie TRIG impuls jest zawsze krótszy, więc długi gate nie włączy żadnej z tych funkcji.

---

## Schemat ideowy

![Schemat](schematic.svg)

## Zasada działania

Przycisk tap w obu pedałach to pin MCU trzymany na ~3.3V — zwarcie do GND oznacza wciśnięcie. Optoizolator PC817 symuluje to zwarcie z pełną izolacją galwaniczną: masa modulara (GND_mod) i masa pedału (GND_ped) nie są połączone, więc nie ma pętli masy ani humu. LED optoizolatora jest zasilana wprost z sygnału CV przez rezystor 470Ω, a tranzystor BC547B w szeregu z LED działa jak „furtka”. Furtkę otwiera filtr HP (0.22µF, 47kΩ, 100kΩ) sterujący bazą tranzystora — dzięki temu każdy gate zamienia się w tap trwający 15–133 ms (tryb TRIG), a w trybie GATE przełącznik omija filtr i tap trwa tyle co gate. Rezystor 47kΩ na wejściu ściąga je do 0V, żeby każdy kolejny gate dawał tap, a diody 1N4148 chronią LED i tranzystor. Obwód nie ma własnego zasilania i wytrzymuje sygnały ±10V (20 Vpp) i ±12V.

---

## Komponenty (na jeden pedał)

Wszystkie elementy przewlekane (THT) — pilnuj obudowy przy zakupie.

| Oznaczenie | Element | Wartość / obudowa | Ilość |
|---|---|---|---|
| OC1, OC2 | Optoizolator | PC817, **DIP-4** (nie PC817S / SMD) | 2 |
| Q1, Q2 | Tranzystor NPN | **BC547B**, TO-92 | 2 |
| D1–D4 | Dioda | 1N4148, **DO-35** | 4 |
| R2, R4 | Rezystor | 470Ω, **0,6 W** | 2 |
| R5, R6, R7, R8 | Rezystor | 47kΩ, 1/4 W | 4 |
| R1, R3 | Rezystor | 100kΩ, 1/4 W | 2 |
| C1, C2 | Kondensator filmowy | 0.22µF, 63V+, radialny, raster 5 mm | 2 |
| SELECT | Toggle ON/OFF/ON | SPDT, mini | 1 |
| GATE/TRIG, REC | Toggle ON/OFF | SPST, mini | 2 |
| — | Gniazdo 3.5mm mono | Thonkiconn PJ398SM | 3 |
| — | Perfboard | 5×7 cm, raster 2.54 mm | 1 |

Zapas na wypadek wymiany: 2× kondensator 0.33µF (jeśli pedał nie łapie krótkich impulsów — patrz plan.md). Pełna lista zakupów na dwa pedały: [plan.md](plan.md), Zadanie 2.

---

## Pliki

- [`spec.md`](spec.md) — specyfikacja v3: źródło prawdy dla wartości, połączeń i kierunków diod; sekcja „Dlaczego v3” opisuje błędy poprzedniej wersji
- [`plan.md`](plan.md) — instrukcja budowy krok po kroku, z pomiarami i punktami przerwy
- [`schematic.svg`](schematic.svg) — schemat ideowy, generowany przez `tools/gen_schematic.py`
- [`sim/`](sim/) — symulacje ngspice; `sim/run.sh` odtwarza wszystkie liczby ze spec.md
- [`tools/check_docs.py`](tools/check_docs.py) — kontrola spójności dokumentów ze spec.md (`python3 tools/check_docs.py`)

---

## Znane ograniczenia

- **Cathedral:** podczas tapowania reverb krótko się urywa — ograniczenie firmware, nie moda
- **Wolne LFO (sinus) w trybie TRIG:** łagodne zbocze daje niepewny tap — do sterowania z LFO używaj trybu GATE albo przebiegu prostokątnego
- **Minimalna długość impulsu**, którą akceptuje MCU pedału, nie jest publikowana — mierzona po zbudowaniu (plan.md); w razie potrzeby wymiana C1/C2 na 0.33µF
- **Próg 350 ms w Cathedral** pochodzi z manuala w wersji, której nie udało się zweryfikować bezpośrednio

---

## Źródła

- [EHX Stereo Memory Man with Hazarai — manual (PDF)](https://www.ehx.com/wp-content/uploads/2021/01/stereo-memory-man-with-hazarai-manual.pdf)
- [EHX Cathedral — manual (ManualsLib)](https://www.manualslib.com/manual/2900221/Electro-Harmonix-Cathedral-Stereo-Reverb.html)
- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
