# CV Tap Tempo Mod — EHX SMMH + EHX Cathedral

**Data:** 2026-05-29  
**Aktualizacja:** 2026-06-04 — izolacja galwaniczna (BC547 → PC817)  
**Status:** Zatwierdzone

---

## Cel

Modyfikacja dwóch pedałów efektów:
- EHX Stereo Memory Man with Hazarai (SMMH)
- EHX Cathedral

Każdy pedał otrzymuje niezależny obwód dodający trzy wejścia CV trigger/gate z Eurorack (standard 0–5V), które sterują funkcją tap tempo. Projekt oparty na modyfikacji navs.modular.lab.

---

## Architektura

Dwa osobne, identyczne obwody — jeden na pedał. Każdy montowany na płytce perforowanej (perfboard) wewnątrz obudowy pedału.

### Zasada działania

Przycisk tap w obu pedałach działa identycznie: pin MCU trzymany wysoko (~3.3V), wciśnięcie przycisku zwiera go do GND. Obwód symuluje to zwarcie przez optoizolator PC817 sterowany sygnałem CV. GND modulara i GND pedału są galwanicznie odizolowane — brak ryzyka pętli masy.

---

## Wejścia i sterowanie

### Wejście A i B (przełączane)
- Dwa gniazda 3.5mm mono
- Przełącznik **SELECT** (3-pozycyjny ON/OFF/ON): wybiera aktywne wejście — A, wyłączone, lub B
- Przełącznik **HP** (2-pozycyjny ON/OFF): włącza/wyłącza filtr górnoprzepustowy dla aktywnego toru A/B
- Oba wejścia mogą mieć podłączone sygnały jednocześnie bez ryzyka — SELECT fizycznie rozłącza nieaktywną gałąź

### Wejście C
- Gniazdo 3.5mm mono
- Zawsze aktywne, nie podlega przełącznikowi SELECT
- Zawsze z filtrem HP (hardwired)

### Przełącznik REC
- 2-pozycyjny ON/OFF
- Bezpośrednie zwarcie tap_pin do GND_pedału — symuluje przytrzymanie przycisku (przydatne w trybie loopera SMMH)

---

## Schemat obwodu

```
─────────────────── STRONA MODULARA (GND_mod) ──────────┬── STRONA PEDAŁU (GND_ped) ───
                                                         │ (izolacja galwaniczna PC817)
CV_A ──┐                                                 │
       ├──[SELECT A/OFF/B]──┬──[0.1µF]──┬──[470Ω]──[D1]──LED(+)[OC1]LED(−)──GND_mod
CV_B ──┘              [SW_HP bypass]   [10kΩ]                 fototranz. C ──► tap_pin
                            │            │                     fototranz. E ──── GND_ped
                            └────────────┘
                                GND_mod

CV_C ──────────────[0.1µF]──┬──[470Ω]──[D2]──LED(+)[OC2]LED(−)──GND_mod
                           [10kΩ]            fototranz. C ──► tap_pin
                            │                fototranz. E ──── GND_ped
                           GND_mod

D1, D2: 1N4148 — antyparalel do LED (katoda D → anoda LED, anoda D → katoda LED)
        (klampuje ujemny spike filtra HP, chroni LED przed reverse breakdown)

REC switch ──────────────────────────────────────────────── tap_pin ──── GND_ped

OC1, OC2: PC817 (DIP-4) — pin 1: LED(+), pin 2: LED(−), pin 3: E, pin 4: C
```

### Filtr górnoprzepustowy (HP)
- RC: C = 0.1µF (serie) + R = 10kΩ (shunt do GND_mod) → f_c = 1/(2π × 10k × 0.1µF) ≈ **160 Hz**
- Stała czasowa τ ≈ 1ms: gate >5ms zostaje skrócony do ~1ms impulsu — nie może wyzwolić trybu loop
- Przełącznik SW_HP: gdy zwarty — sygnał CV omija kondensator, idzie prosto do LED; gdy rozwarty — sygnał przez filtr RC
- Cały filtr HP po stronie modulara — izolacja galwaniczna zachowana

**Uwaga:** kondensator 0.1µF powinien być filmowy (nieelektrolityczny) ze względu na brak spolaryzowanego sygnału i małą pojemność.

### Rezystor LED (470Ω)
- Przy CV = 5V: I_LED = (5V − 1.2V) / 470Ω ≈ **8 mA** — pewne wysterowanie PC817
- Przy CV = 10V: I_LED = (10V − 1.2V) / 470Ω ≈ **18.7 mA** — w normie (max LED PC817 = 50 mA)
- CTR PC817 ≥ 100% przy 5 mA → fototranzystor nasyca się pewnie przy 8 mA

---

## Lista komponentów (na jeden pedał)

| Element | Wartość | Ilość |
|---|---|---|
| Optoizolator | PC817 (DIP-4) | 2 |
| Dioda | 1N4148 | 2 |
| Rezystor | 10kΩ | 2 |
| Rezystor | 470Ω | 2 |
| Kondensator filmowy | 0.1µF | 2 |
| Przełącznik 3-poz. ON/OFF/ON | dowolny mini toggle | 1 |
| Przełącznik 2-poz. ON/OFF | dowolny mini toggle | 2 |
| Gniazdo 3.5mm mono | Cliff S2 lub Thonkiconn | 3 |
| Płytka perforowana | ~3×4 cm | 1 |

**Łącznie na oba pedały:** ×2 każdego elementu.

---

## Montaż

1. Wywiercić otwory w obudowie pedału na 3 gniazda 3.5mm i 3 przełączniki
2. Zmontować obwód na perfboardzie
3. Zlokalizować na PCB pedału punkty lutownicze przycisku tap (dwa pady: tap_pin i GND_ped)
4. Podłączyć pin 4 (C) PC817 do tap_pin, pin 3 (E) do GND_pedału
5. Pin 2 (LED−) PC817 do GND_modulara (sleeve gniazda 3.5mm)
6. Przełącznik REC bezpośrednio między tap_pin a GND_pedału

---

## Weryfikacja elektryczna

- **SMMH:** potwierdzone — tap działa jak Cathedral (zwarcie tap_pin do GND)
- **Cathedral:** potwierdzone — tap_pin siedzi na 3.3V, wciśnięcie zwiera do GND
- PC817 zapewnia pełną izolację galwaniczną — CV nie dociera do tap_pin, GND modulara nie łączy się z GND pedału
- D1/D2 (1N4148 antyparalel do LED): klampują ujemny spike filtra HP — chroni LED przed reverse breakdown (~5V)
- Rezystor 470Ω: zapewnia I_LED ≈ 8 mA przy 5V CV, pewne wysterowanie fototranzystora

---

## Znane ograniczenia

- **Cathedral:** podczas tapowania reverb krótko się urywa — ograniczenie firmware Cathedral, nie obwodu
- **REC w SMMH** wchodzi w tryb loopera — celowe, ale wymaga świadomości przy graniu

---

## Źródła

- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
