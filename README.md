# CV Tap Tempo Mod — EHX SMMH + Cathedral

Modyfikacja sprzętowa dodająca wejścia CV trigger/gate z Eurorack do funkcji tap tempo w pedałach:

- **EHX Stereo Memory Man with Hazarai** (delay)
- **EHX Cathedral** (reverb)

Projekt oparty na modyfikacji [navs.modular.lab](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html).

---

## Co robi ten mod

Każdy pedał otrzymuje trzy wejścia CV 3.5mm (standard Eurorack 0–5V):

| Wejście | Opis |
|---|---|
| **A** | Trigger/gate, przełączane przez SELECT |
| **B** | Trigger/gate, przełączane przez SELECT |
| **C** | Zawsze aktywne, zawsze z filtrem HP |

Oraz trzy przełączniki:

| Przełącznik | Funkcja |
|---|---|
| **SELECT** (ON/OFF/ON) | Wybór aktywnego wejścia: A / wyłączone / B |
| **HP** (ON/OFF) | Filtr górnoprzepustowy dla toru A/B (blokuje DC i long gates) |
| **REC** (ON/OFF) | Przytrzymanie tap — wejście w tryb loopera (SMMH) |

---

## Zasada działania

Przycisk tap w obu pedałach to pin MCU trzymany na ~3.3V, zwarcie do GND = wciśnięcie. Obwód używa tranzystorów NPN (BC547) do symulowania tego zwarcia. Filtr HP (RC: 0.1µF + 10kΩ, f_c ≈ 160 Hz, τ ≈ 1ms) skraca długie gate'y do krótkich impulsów, zapobiegając przypadkowemu wejściu pedału w tryb loopera.

```
CV ──[0.1µF]──┬──[1kΩ]──── B ┐
             [10kΩ]           │ BC547
              │               C ──── tap_pin pedału
             GND              E ──── GND
```

---

## Komponenty (na jeden pedał)

| Element | Wartość | Ilość |
|---|---|---|
| Tranzystor NPN | BC547B lub 2N3904 | 2 |
| Rezystor | 10kΩ, 1/4W | 2 |
| Rezystor | 1kΩ, 1/4W | 2 |
| Kondensator filmowy | 0.1µF (WIMA MKS2 lub ekw.) | 2 |
| Toggle switch 3-poz | ON/OFF/ON, SPDT, mini | 1 |
| Toggle switch 2-poz | ON/OFF, SPST, mini | 2 |
| Gniazdo 3.5mm | Thonkiconn PJ398SM lub Cliff FC68131 | 3 |
| Perfboard | ~4×5 cm, raster 2.54mm | 1 |

---

## Pliki

- [`spec.md`](spec.md) — pełna specyfikacja projektu (projekt obwodu, logika przełączania, weryfikacja elektryczna)
- [`plan.md`](plan.md) — plan implementacji krok po kroku (BOM, layout perfboard, montaż, testy)

---

## Znane ograniczenia

- **Cathedral:** podczas tapowania reverb krótko się urywa — ograniczenie firmware, nie moda
- **Brak izolacji galwanicznej** — GND modulara = GND pedału; jeśli pojawi się hum, BC547 można zastąpić optoizolatorem PC817

---

## Źródła

- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
