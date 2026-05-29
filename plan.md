# CV Tap Tempo Mod — EHX SMMH + Cathedral — Plan Implementacji

> **Dla tego projektu:** to projekt sprzętowy, nie softwarowy. Zamiast TDD używamy weryfikacji multimetrem i testów funkcjonalnych. Każde zadanie kończy się checkpointem pomiarowym przed przejściem dalej.

**Cel:** Zainstalować w obu pedałach obwód CV tap tempo (3 wejścia A/B/C + SELECT + HP + REC) na perfboardzie wewnątrz obudów.

**Architektura:** Dwa tranzystory NPN (BC547) per pedał symulują zwarcie przycisku tap do GND. Filtr HP (RC: 0.1µF + 10kΩ) skraca gate'y do ~1ms, zapobiegając wejściu w tryb loopera. Wejścia A/B przełączane przełącznikiem SELECT (ON/OFF/ON). Wejście C zawsze aktywne.

**Sprzęt:** multimetr, lutownica, perfboard, BC547, kondensatory filmowe 0.1µF, rezystory 10kΩ/1kΩ, mini toggle switches, gniazda 3.5mm Thonkiconn

---

## Zadanie 1: Lista zakupów i weryfikacja komponentów

**Elementy:** zakupy online (TME, Mouser, Botland) lub lokalny sklep elektroniczny

- [ ] **Krok 1: Zamów lub skompletuj komponenty**

  **Lista na dwa pedały (podwójne ilości):**

  | Element | Specyfikacja | Ilość | Gdzie kupić |
  |---|---|---|---|
  | Tranzystor NPN | BC547B lub 2N3904 | 4 szt | TME / Botland |
  | Rezystor | 10kΩ, 1/4W, metal film | 4 szt | TME / Botland |
  | Rezystor | 1kΩ, 1/4W, metal film | 4 szt | TME / Botland |
  | Kondensator filmowy | 0.1µF, 63V+ (WIMA MKS2 lub Vishay) | 4 szt | TME / Mouser |
  | Przełącznik toggle 3-poz | ON/OFF/ON, SPDT, mini, gwint 6mm | 2 szt | TME (np. SCI R13-73B) |
  | Przełącznik toggle 2-poz | ON/OFF, SPST, mini, gwint 6mm | 4 szt | TME |
  | Gniazdo 3.5mm | Thonkiconn (PJ398SM) lub Cliff FC68131 | 6 szt | Thonk.co.uk / Modular Addict |
  | Perfboard | 4×6 cm, rastrowanie 2.54mm | 2 szt | Botland |
  | Drut do montażu | 0.3mm izolowany, kilka kolorów | 1 zestaw | — |
  | Nakrętki M3 + podkładki | do mocowania perfboardu | 8 szt | — |

- [ ] **Krok 2: Sprawdź BC547 multimetrem (test diodowy)**

  Ustaw multimetr na tryb diodowy (symbol diody).
  Flat side tranzystora skierowana w swoją stronę, nóżki w dół: kolejność C–B–E (lewa–środkowa–prawa).

  - Czerwona sonda na B (środkowa), czarna na E → odczyt ~0.6–0.7V ✓
  - Czerwona sonda na B, czarna na C → odczyt ~0.6–0.7V ✓
  - Wszystkie inne kombinacje → OL (brak przewodzenia) ✓

  Jeśli któryś tranzystor pokazuje inne wartości — wyrzuć, użyj kolejnego.

- [ ] **✓ Checkpoint 1:** Wszystkie komponenty na stole, tranzystory zweryfikowane.

---

## Zadanie 2: Zlokalizowanie padów tap w obu pedałach

**Uwaga:** Wykonaj to PRZED jakimkolwiek wierceniem. Potrzebujesz znać dokładne miejsce połączenia wewnątrz pedału, żeby dobrać długość kabli.

### SMMH

- [ ] **Krok 1: Otwórz SMMH**

  Odkręć śruby na spodzie obudowy. Płytka jest przymocowana do potencjometrów — wyciągaj ostrożnie, nie ciągnij za przewody.

- [ ] **Krok 2: Zlokalizuj przycisk TAP**

  Przycisk TAP to mały przełącznik chwilowy (tact switch) na PCB, opisany "TAP" lub podłączony do przycisku na obudowie. Na SMMH jest to przycisk po prawej stronie panelu górnego.

- [ ] **Krok 3: Zmierz napięcie na padach tap**

  Ustaw multimetr na DC 20V. Jeden sond na GND pedału (masa — np. zewnętrzna obudowa jack audio). Drugi sond po kolei na oba pady przycisku tap.

  Oczekiwany wynik:
  - Jeden pad: ~3.3V (to jest **tap_pin** — pin MCU)
  - Drugi pad: 0V (to jest **GND**)

  Przy wciśniętym przycisku tap: tap_pin spada do ~0V ✓

  Zaznacz/sfotografuj który pad to tap_pin, który GND.

- [ ] **Krok 4: Zamknij SMMH tymczasowo**

### Cathedral

- [ ] **Krok 5: Otwórz Cathedral**

  Analogicznie — śruby na spodzie.

- [ ] **Krok 6: Zlokalizuj przycisk TAP**

  Przycisk TAP w Cathedral jest po lewej stronie panelu (obok pokrętła Reverb Time). Znajdź tact switch na PCB lub pady gdzie jest do niego dolutowany kabelek.

- [ ] **Krok 7: Zmierz napięcie (identycznie jak SMMH)**

  Oczekiwany wynik identyczny: jeden pad ~3.3V (tap_pin), drugi 0V (GND).

  Zaznacz/sfotografuj.

- [ ] **Krok 8: Zamknij Cathedral tymczasowo**

- [ ] **✓ Checkpoint 2:** Znasz dokładne pady tap_pin i GND w obu pedałach.

---

## Zadanie 3: Budowa obwodu na perfboardzie (jeden egzemplarz, potem drugi)

Buduj oba pedały osobno (dwa identyczne perfboardy). Poniższy layout jest na jeden pedał.

**Schemat elektryczny do zbudowania:**

```
                    ┌──[0.1µF C1]──────────────────┐
SELECT_common ──────┤                              node_AB
                    └──[SW_HP bypass]──────────────┘
                                                    │
                                                  [10kΩ R1]
                                                    │
                                                   GND
                                                    │
                              node_AB ──[1kΩ R2]──B─┤
                                                    │ TR1 (BC547)
                              tap_pin ─────────────C─┤
                              GND ─────────────────E─┘

CV_C_jack ──[0.1µF C2]──────────────────────────node_C
                                                    │
                                                  [10kΩ R3]
                                                    │
                                                   GND
                                                    │
                              node_C ───[1kΩ R4]──B─┤
                                                    │ TR2 (BC547)
                              tap_pin ─────────────C─┘
                              GND ─────────────────E─┘

REC switch: bezpośrednio tap_pin ↔ GND (zwarcie)
```

**BC547 pinout** (flat side skierowana w twoją stronę, nóżki wskazują w dół): C – B – E (lewa–środkowa–prawa)

### Layout na perfboardzie (rastrowanie 2.54mm)

```
Kolumny:  1   2   3   4   5   6   7   8   9   10
Rząd A:  [GND rail ─────────────────────────────]
Rząd B:  [    ] [C1+] [C1-] [R1] [   ] [R2] [TR1-C] [TR1-B] [TR1-E→GND]
Rząd C:  [    ] [C2+] [C2-] [R3] [   ] [R4] [TR2-C] [TR2-B] [TR2-E→GND]
Rząd D:  [GND rail ─────────────────────────────]
```

Uproszczony opis rozmieszczenia:
- Rząd A i D: szyna GND (połączone drut na spodzie)
- TR1 i TR2: wzdłuż rzędu B i C, kolumny 7–9
- C1, C2: kondensatory filmowe, pionowo, kolumny 2–3
- R1, R3 (10kΩ shunt): od node (po cap) do GND rail
- R2, R4 (1kΩ base): od node do bazy tranzystora

- [ ] **Krok 1: Przygotuj perfboard**

  Odetnij perfboard na ~4×5 cm (ok. 15×20 otworów). Zaznacz markerem szyny GND wzdłuż górnej i dolnej krawędzi.

- [ ] **Krok 2: Wlutuj tranzystory TR1 i TR2**

  Umieść TR1 w rzędzie B (kolumny 7–9), TR2 w rzędzie C (kolumny 7–9). Flat side do siebie. Sprawdź orientację (C–B–E). Wlutuj. Nie przegrzewaj — max 3 sekundy na nóżkę.

  Zmierz multimetrem: kolektor–emiter w trybie diodowym → OL (nie zwarte). ✓

- [ ] **Krok 3: Wlutuj rezystory shunt (R1, R3 = 10kΩ)**

  Pionowo. Jeden koniec: node po kapacytorze. Drugi koniec: GND rail. Przyciąć nóżki krótko.

- [ ] **Krok 4: Wlutuj kondensatory filmowe (C1, C2 = 0.1µF)**

  Filmowe są niepolarne — orientacja dowolna. Jeden koniec: wejście (od SELECT/od CV_C). Drugi: do node_AB / node_C.

- [ ] **Krok 5: Wlutuj rezystory bazowe (R2, R4 = 1kΩ)**

  Od node_AB / node_C do bazy (pin środkowy) TR1/TR2.

- [ ] **Krok 6: Połącz emitory do GND**

  Drut od E (prawa nóżka) TR1 i TR2 do GND rail.

- [ ] **Krok 7: Połącz kolektory — pozostaw na razie jako wolne końce drutów**

  Drut ~10 cm od C TR1 i C TR2 — to będzie podłączone do tap_pin pedału. Oznacz (np. czerwony).

  Podobnie: drut od GND rail (drugie połączenie do GND pedału). Oznacz czarny.

- [ ] **Krok 8: Wyprowadź drut od node_AB na zewnątrz**

  To jest wejście od przełącznika SELECT (common). Drut ~10 cm, oznacz żółty.

- [ ] **Krok 9: Wyprowadź drut od node_C**

  Wejście z CV_C jack. Drut ~10 cm, oznacz niebieski.

- [ ] **✓ Checkpoint 3: Test wizualny**

  Sprawdź pod lupą każde połączenie lutownicze: brak mostków między padami, brak zimnych spoin (matowe, kruszące się lutowie = zimna spoina — przetop).

---

## Zadanie 4: Test elektryczny perfboardu (przed instalacją w pedale)

- [ ] **Krok 1: Test ciągłości szyny GND**

  Multimetr w trybie ciągłości (sygnał dźwiękowy). Sonda na GND rail lewa → sonda na GND rail prawa → sygnał dźwiękowy ✓

- [ ] **Krok 2: Test izolacji kolektor–emiter (tranzystor wyłączony)**

  Ustaw DC 5V (lub użyj zasilacza 5V / baterii 4.5V).
  Podłącz: + do kolektora TR1 przez rezystor 10kΩ (ochronny), – do emitera (GND).
  Baza TR1: niepodłączona (lub przez 100kΩ do GND).

  Zmierz napięcie na kolektorze: powinno być ~5V (tranzystor zamknięty, prąd nie płynie) ✓

- [ ] **Krok 3: Test przełączenia tranzystora**

  Podaj +5V przez rezystor 1kΩ na bazę TR1.
  Zmierz napięcie na kolektorze: powinno spaść do <0.3V (tranzystor otwarty, zwiera kolektor do GND) ✓

  Powtórz dla TR2.

- [ ] **Krok 4: Test filtra HP**

  Podaj wolny gate (np. 1Hz, 1V) na wejście C1. Zmierz na node_AB:
  - Powinien pojawić się krótki impuls (~1ms) na każdym zboczu wejścia ✓
  - (Lub sprawdź oscyloskopem jeśli dostępny — nie jest wymagany)

  Alternatywnie: podaj stały +5V na wejście przez C1 → napięcie na node_AB powinno opaść do 0V po ok. 1ms (τ = RC = 10k × 0.1µF = 1ms) ✓

- [ ] **✓ Checkpoint 4:** Oba tranzystory przełączają poprawnie. Filtr HP działa.

---

## Zadanie 5: Przygotowanie obudowy pedału (wiercenie)

Wykonaj dla każdego pedału z osobna. Zacznij od SMMH.

- [ ] **Krok 1: Zaplanuj rozmieszczenie otworów**

  Narysuj rozkład na obudowie ołówkiem/taśmą:
  - 3× otwór 6.5mm (lub wg średnicy Thonkiconn / Cliff) na gniazda 3.5mm
  - 3× otwór 6mm na przełączniki toggle
  - 1× opcjonalny otwór M3 na mocowanie perfboardu

  Sprawdź że otwory nie kolidują z komponentami wewnątrz (spójrz przez istniejące otwory lub zmierz).

- [ ] **Krok 2: Wywierć otwory pilotażowe 2mm**

  Użyj wiertarki ręcznej lub Dremel. Wywierć najpierw małe otwory pilotażowe w zaznaczonych punktach.

- [ ] **Krok 3: Rozwiercić do docelowej średnicy**

  Stopniowo zwiększaj wiertło: 2mm → 4mm → 6.5mm (dla jacków) i 6mm (dla toggles).
  Pilnikiem usuń zadziory z otworów.

- [ ] **Krok 4: Przymierz komponenty**

  Wsuń gniazda i przełączniki w otwory (bez przykręcania). Sprawdź że pasują i nie kolidują z PCB pedału.

- [ ] **✓ Checkpoint 5:** Wszystkie otwory wywierconee, komponenty pasują.

---

## Zadanie 6: Instalacja w SMMH

- [ ] **Krok 1: Przylutuj przewody do padów tap SMMH**

  Otwórz SMMH (jak w Zadaniu 2). Na wcześniej zidentyfikowanych padach:
  - tap_pin pad: przylutuj czerwony drut ~15 cm
  - GND pad: przylutuj czarny drut ~15 cm

  Użyj minimum cyny. Nie ruszaj sąsiednich komponentów.

- [ ] **Krok 2: Zmontuj gniazda 3.5mm w otworach**

  Przykręć Thonkiconn / Cliff przez obudowę. Przylutuj:
  - Jack A: tip → do jednej pozycji SELECT switch (np. lewa)
  - Jack B: tip → do drugiej pozycji SELECT switch (prawa)
  - Jack C: tip → do node_C wejścia na perfboardzie (niebieski drut)
  - Wszystkie sleeve (masa jacka): wspólny GND

- [ ] **Krok 3: Zmontuj przełącznik SELECT (3-poz ON/OFF/ON)**

  SPDT center-off. Podłącz:
  - Lewy terminal: CV_A (tip jacka A)
  - Prawy terminal: CV_B (tip jacka B)
  - Środkowy (common): żółty drut → wejście C1 na perfboardzie (node_AB input)

- [ ] **Krok 4: Zmontuj przełącznik HP (2-poz ON/OFF)**

  SPST. Podłącz:
  - Terminal 1: input C1 (wejście od SELECT common)
  - Terminal 2: output C1 (node_AB, za kondensatorem)
  - Gdy zwarty (ON): bypass caps filtra HP ✓

- [ ] **Krok 5: Zmontuj przełącznik REC (2-poz ON/OFF)**

  SPST. Podłącz bezpośrednio:
  - Terminal 1: czerwony drut od tap_pin
  - Terminal 2: czarny drut GND

- [ ] **Krok 6: Podłącz perfboard do tap_pin i GND**

  - Kolektor TR1 i TR2 (połączone razem) → czerwony drut → tap_pin SMMH
  - GND rail perfboardu → czarny drut → GND SMMH

- [ ] **Krok 7: Przymocuj perfboard wewnątrz obudowy**

  Klej termiczny lub dystansowniki M3. Upewnij się że perfboard nie dotyka PCB SMMH.

- [ ] **✓ Checkpoint 6:** SMMH złożony, wszystkie połączenia wykonane.

---

## Zadanie 7: Test funkcjonalny SMMH

- [ ] **Krok 1: Test REC switch**

  Zamknij SMMH (lub trzymaj otwarty ostrożnie). Podłącz zasilanie.
  Włącz przełącznik REC → SMMH powinien wejść w tryb loopera (przytrzymanie tap). ✓
  Wyłącz REC → powrót do normalnej pracy. ✓

- [ ] **Krok 2: Test ręczny wejścia CV**

  Użyj kawałka drutu: zewrzyj tip jacka C do GND (symulacja triggera 0V→0V→0V).
  Alternatywnie: przyłóż +3.3–5V między tip C a sleeve.

  Podaj kilka krótkich zwarć (1 per sekunda) → SMMH powinien traktować je jako tap tempo. ✓

  Sprawdź też wejścia A i B przez przełącznik SELECT.

- [ ] **Krok 3: Test z modularze (jeśli dostępny)**

  Podłącz kabel patch z outputu gate/trigger modularze do jacka C.
  Ustaw SMMH w tryb delay. Wyślij regularny trigger (np. z sekwencera lub LFO).
  Delay powinien zsynchronizować się z tempem triggera. ✓

- [ ] **Krok 4: Test filtra HP**

  Podaj stały gate (ciągłe +5V) na wejście C. SMMH nie powinien wejść w tryb loopera (filtr HP blokuje DC). ✓
  Podaj krótkie pulsy (<10ms) → normalnie triggeruje tap. ✓

- [ ] **✓ Checkpoint 7:** SMMH działa poprawnie. Zamknij obudowę.

---

## Zadanie 8: Instalacja i test w Cathedral

Identyczny przebieg jak Zadania 6–7, tylko dla Cathedral.

- [ ] **Krok 1: Przylutuj przewody do padów tap Cathedral** (jak Krok 1 z Zadania 6)
- [ ] **Krok 2: Zmontuj gniazda 3.5mm** (jak Krok 2)
- [ ] **Krok 3: Zmontuj SELECT switch** (jak Krok 3)
- [ ] **Krok 4: Zmontuj HP switch** (jak Krok 4)
- [ ] **Krok 5: Zmontuj REC switch** (jak Krok 5)
- [ ] **Krok 6: Podłącz perfboard** (jak Krok 6)
- [ ] **Krok 7: Przymocuj perfboard** (jak Krok 7)
- [ ] **Krok 8: Test REC, test ręczny wejść A/B/C** (jak Zadanie 7, kroki 1–4)

  **Dodatkowa uwaga dla Cathedral:** podczas tapowania reverb krótko się urywa — to normalne zachowanie firmware Cathedral, nie błąd moda.

- [ ] **✓ Checkpoint 8:** Cathedral działa poprawnie. Zamknij obudowę.

---

## Znane ryzyka i troubleshooting

| Objaw | Możliwa przyczyna | Rozwiązanie |
|---|---|---|
| Tap w ogóle nie działa z CV | Błędna identyfikacja tap_pin/GND | Zamierz ponownie z zasilaniem; sprawdź czy tap_pin i GND nie są zamienione |
| Hum / pętla masy | GND modulara = GND pedału (brak izolacji) | Dodaj optoizolator PC817 zamiast BC547 |
| Pedał wchodzi w tryb loop przy długich gate'ach | Filtr HP nie skraca gate | Sprawdź C1 (czy filmowy, nie elektrolityczny); sprawdź node_AB |
| Trigger działa tylko raz | Kondensator nie zdążył się rozładować | Zwiększ rezystor shunt do 47kΩ (dłuższy czas rozładowania) |
| SELECT switch nie przełącza | Błędne podłączenie terminali SPDT | Zamierz ciągłość między common a lewym/prawym terminalem |

---

## Źródła i referencje

- [Spec projektu](../specs/2026-05-29-cv-tap-tempo-mod-design.md)
- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
