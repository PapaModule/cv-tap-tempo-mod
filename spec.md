# CV Tap Tempo Mod — EHX SMMH + EHX Cathedral

**Data:** 2026-05-29  
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

Przycisk tap w obu pedałach działa identycznie: pin MCU trzymany wysoko (~3.3V), wciśnięcie przycisku zwiera go do GND. Obwód symuluje to zwarcie przez tranzystor NPN sterowany sygnałem CV.

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
- Bezpośrednie zwarcie tap_pin do GND — symuluje przytrzymanie przycisku (przydatne w trybie loopera SMMH)

---

## Schemat obwodu

```
CV_A ──┐
       ├──[SELECT A/OFF/B]──┬──[0.1µF]──┬──[1kΩ]──baza TR1 ──┐
CV_B ──┘                   │           [10kΩ]                   │
                     [SW_HP bypass]      │                       │
                           │            GND                      ├──► tap_pin pedału
                           └────────────┘ (bypass: SW_HP zwarty)│
                                                                 │
CV_C ──[0.1µF]──┬──[1kΩ]──────────────────────────baza TR2 ──┘
               [10kΩ]
                │
               GND

REC switch ──────────────────────────────────────────────────────► tap_pin (zwarcie)

TR1, TR2: kolektor → tap_pin | emiter → GND pedału
```

### Filtr górnoprzepustowy (HP)
- RC: C = 0.1µF (serie) + R = 10kΩ (shunt do GND) → f_c = 1/(2π × 10k × 0.1µF) ≈ **160 Hz**
- Stała czasowa τ ≈ 1ms: gate >5ms zostaje skrócony do ~1ms impulsu — nie może wyzwolić trybu loop
- Przełącznik SW_HP: gdy zwarty (OFF) — sygnał CV omija kondensator, idzie prosto do bazy; gdy rozwarty (ON) — sygnał przez filtr RC

**Uwaga:** kondensator 0.1µF powinien być filmowy (nieelektrolityczny) ze względu na brak spolaryzowanego sygnału i małą pojemność.

---

## Lista komponentów (na jeden pedał)

| Element | Wartość | Ilość |
|---|---|---|
| Tranzystor NPN | BC547 (lub 2N3904) | 2 |
| Rezystor | 10kΩ | 2 |
| Rezystor | 1kΩ | 2 |
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
3. Zlokalizować na PCB pedału punkty lutownicze przycisku tap (dwa pady: tap_pin i GND)
4. Podłączyć kolektor TR1/TR2 do tap_pin, emiter do GND pedału
5. Przełącznik REC bezpośrednio między tap_pin a GND

---

## Weryfikacja elektryczna

- **SMMH:** potwierdzone — tap działa jak Cathedral (zwarcie tap_pin do GND)
- **Cathedral:** potwierdzone — tap_pin siedzi na 3.3V, wciśnięcie zwiera do GND
- Tranzystor nie łączy CV z tap_pin (izolacja przez topologię — CV tylko na bazie)
- Diody klampujące pominięte — zbędne przy tej topologii
- Brak izolacji galwanicznej (GND modulara = GND pedału) — akceptowalne; w razie problemów z humem zastąpić BC547 optoizolatorem PC817

---

## Znane ograniczenia

- **Cathedral:** podczas tapowania reverb krótko się urywa — ograniczenie firmware Cathedral, nie obwodu
- **Brak izolacji galwanicznej** — możliwa pętla masy przy niektórych konfiguracjach rack/pedalboard
- **REC w SMMH** wchodzi w tryb loopera — celowe, ale wymaga świadomości przy graniu

---

## Źródła

- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
