# CV Tap Tempo Mod — EHX SMMH + Cathedral — Plan Implementacji

> **Dla tego projektu:** to projekt sprzętowy, nie softwarowy. Zamiast TDD używamy weryfikacji multimetrem i testów funkcjonalnych. Każde zadanie kończy się checkpointem pomiarowym przed przejściem dalej.

**Cel:** Zainstalować w obu pedałach obwód CV tap tempo (3 wejścia A/B/C + SELECT + HP + REC) na perfboardzie wewnątrz obudów.

**Architektura:** Dwa optoizolatory PC817 (DIP-4) per pedał symulują zwarcie przycisku tap do GND z pełną izolacją galwaniczną. GND modulara (GND_mod) i GND pedału (GND_ped) nie są połączone — eliminuje pętle masy. Filtr HP (RC: 0.1µF + 10kΩ) skraca gate'y do ~1ms. Wejścia A/B przełączane przez SELECT (ON/OFF/ON). Wejście C zawsze aktywne.

**Sprzęt:** multimetr, lutownica, perfboard, PC817 (DIP-4), kondensatory filmowe 0.1µF, rezystory 10kΩ/470Ω, 1N4148, mini toggle switches, gniazda 3.5mm Thonkiconn

---

## Zadanie 1: Lista zakupów i weryfikacja komponentów

**Elementy:** zakupy online (TME, Mouser, Botland) lub lokalny sklep elektroniczny

- [ ] **Krok 1: Zamów lub skompletuj komponenty**

  **Lista na dwa pedały (podwójne ilości):**

  | Element | Specyfikacja | Ilość | Gdzie kupić |
  |---|---|---|---|
  | Optoizolator | PC817 (DIP-4) | 4 szt | TME / Botland |
  | Dioda małosygnałowa | 1N4148 | 4 szt | TME / Botland |
  | Rezystor | 10kΩ, 1/4W, metal film | 4 szt | TME / Botland |
  | Rezystor | 470Ω, 1/4W, metal film | 4 szt | TME / Botland |
  | Kondensator filmowy | 0.1µF, 63V+ (WIMA MKS2 lub Vishay) | 4 szt | TME / Mouser |
  | Przełącznik toggle 3-poz | ON/OFF/ON, SPDT, mini, gwint 6mm | 2 szt | TME (np. SCI R13-73B) |
  | Przełącznik toggle 2-poz | ON/OFF, SPST, mini, gwint 6mm | 4 szt | TME |
  | Gniazdo 3.5mm | Thonkiconn (PJ398SM) lub Cliff FC68131 | 6 szt | Thonk.co.uk / Modular Addict |
  | Perfboard | 4×6 cm, rastrowanie 2.54mm | 2 szt | Botland |
  | Drut do montażu | 0.3mm izolowany, kilka kolorów | 1 zestaw | — |
  | Nakrętki M3 + podkładki | do mocowania perfboardu | 8 szt | — |

- [ ] **Krok 2: Sprawdź PC817 multimetrem (test diodowy LED)**

  Ustaw multimetr na tryb diodowy (symbol diody).
  PC817 DIP-4 — trzymaj chip z nacięciem po lewej stronie: piny od lewej to 1, 2, 3, 4.

  - Czerwona sonda na pin 1 (LED+), czarna na pin 2 (LED−) → odczyt ~1.0–1.3V ✓ (dioda LED)
  - Odwrotnie → OL (brak przewodzenia) ✓
  - Pin 4 (C) i pin 3 (E): multimetr w trybie diodowym, czerwona na 4, czarna na 3 → OL (fototranzystor wyłączony, brak światła) ✓

  Jeśli LED nie przewodzi lub C–E zwarte — chip uszkodzony, wymień.

- [ ] **✓ Checkpoint 1:** Wszystkie komponenty na stole, PC817 zweryfikowane.

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
  - Drugi pad: 0V (to jest **GND_ped**)

  Przy wciśniętym przycisku tap: tap_pin spada do ~0V ✓

  Zaznacz/sfotografuj który pad to tap_pin, który GND_ped.

- [ ] **Krok 4: Zamknij SMMH tymczasowo**

### Cathedral

- [ ] **Krok 5: Otwórz Cathedral**

  Analogicznie — śruby na spodzie.

- [ ] **Krok 6: Zlokalizuj przycisk TAP**

  Przycisk TAP w Cathedral jest po lewej stronie panelu (obok pokrętła Reverb Time). Znajdź tact switch na PCB lub pady gdzie jest do niego dolutowany kabelek.

- [ ] **Krok 7: Zmierz napięcie (identycznie jak SMMH)**

  Oczekiwany wynik identyczny: jeden pad ~3.3V (tap_pin), drugi 0V (GND_ped).

  Zaznacz/sfotografuj.

- [ ] **Krok 8: Zamknij Cathedral tymczasowo**

- [ ] **✓ Checkpoint 2:** Znasz dokładne pady tap_pin i GND_ped w obu pedałach.

---

## Zadanie 3: Budowa obwodu na perfboardzie (jeden egzemplarz, potem drugi)

Buduj oba pedały osobno (dwa identyczne perfboardy). Poniższy layout jest na jeden pedał.

**WAŻNE:** Na perfboardzie są DWA osobne GND — nie łącz ich ze sobą:
- **GND_mod** — masa modulara: sleeve jacków, shunt R1/R3, katoda LED PC817 (pin 2)
- **GND_ped** — masa pedału: emiter fototranzystora PC817 (pin 3), REC switch

**Schemat elektryczny do zbudowania:**

```
─────────────── STRONA MODULARA (GND_mod) ──────────┬────── STRONA PEDAŁU (GND_ped) ──
                                                     │ PC817 izolacja galwaniczna
         ┌──[C1: 0.1µF]──────────────────┐           │
SELECT ──┤                             node_AB        │
         └──[SW_HP bypass]─────────────┘             │
                                        │            │
                                      [R1: 10kΩ]     │
                                        │            │
                                      GND_mod        │
                                        │            │
                    node_AB ──[R2: 470Ω]──[D1⟂]──pin1(+)[OC1]pin2(−)──GND_mod
                                                     pin4(C) ──► tap_pin
                                                     pin3(E) ──── GND_ped

CV_C ──[C2: 0.1µF]────────────────── node_C
                                        │
                                      [R3: 10kΩ]
                                        │
                                      GND_mod
                                        │
                    node_C ───[R4: 470Ω]──[D2⟂]──pin1(+)[OC2]pin2(−)──GND_mod
                                                     pin4(C) ──► tap_pin
                                                     pin3(E) ──── GND_ped

D1, D2: 1N4148 antyparalel do LED (katoda D → anoda LED, anoda D → katoda LED)

REC switch: bezpośrednio tap_pin ↔ GND_ped
```

**PC817 DIP-4 pinout** (nacięcie po lewej): pin1=LED+, pin2=LED−, pin3=E, pin4=C

### Layout na perfboardzie (rastrowanie 2.54mm)

```
Kolumny:  1    2    3    4    5    6    7    8    9   10   11   12
Rząd A:  [GND_mod rail ─────────────────────────────────────────]
Rząd B:  [C1+][C1-][    ][R1↕][    ][R2→][D1⟂][OC1-12][OC1-43][    ][tap_pin drut]
Rząd C:  [C2+][C2-][    ][R3↕][    ][R4→][D2⟂][OC2-12][OC2-43][    ][tap_pin drut]
Rząd D:  [GND_ped rail ─────────────────────────── (tylko pin3 OC1, OC2, REC) ────]
```

- Rząd A: szyna GND_mod (sleeve jacków, pin2 PC817, shunt R1/R3)
- Rząd D: szyna GND_ped (pin3 emiter PC817, REC switch)
- Szyny A i D NIE są połączone ze sobą

- [ ] **Krok 1: Przygotuj perfboard**

  Odetnij perfboard na ~4×5 cm (ok. 15×20 otworów). Zaznacz markerem dwie szyny: GND_mod (górna, czerwona linia) i GND_ped (dolna, czarna linia). Opisz je markerem.

- [ ] **Krok 2: Wlutuj optoizolatory OC1 i OC2 (PC817)**

  Umieść OC1 w rzędzie B (kolumny 8–9), OC2 w rzędzie C (kolumny 8–9). Nacięcie chipu skierowane w lewo (pin1 na górze-lewo). Wlutuj. Nie przegrzewaj — max 3 sekundy na nóżkę.

  Zmierz multimetrem: pin4(C)–pin3(E) w trybie diodowym → OL (nie zwarte, brak światła) ✓

- [ ] **Krok 3: Wlutuj rezystory shunt (R1, R3 = 10kΩ)**

  Pionowo. Jeden koniec: node_AB / node_C. Drugi koniec: GND_mod rail.

- [ ] **Krok 4: Wlutuj kondensatory filmowe (C1, C2 = 0.1µF)**

  Filmowe są niepolarne — orientacja dowolna. Jeden koniec: wejście (od SELECT / od CV_C jack). Drugi: node_AB / node_C.

- [ ] **Krok 5: Wlutuj rezystory LED (R2, R4 = 470Ω)**

  Od node_AB / node_C w kierunku pin1(LED+) PC817. Między R2/R4 a pin1 wlutuj D1/D2.

- [ ] **Krok 6: Wlutuj diody D1, D2 (1N4148 antyparalel)**

  Uwaga na orientację — antyparalel do LED oznacza:
  - Katoda D (pierścień) → strona pin1 PC817 (anoda LED)
  - Anoda D → strona R2/R4 (przed LED)

  Dioda jest równoległa do LED, ale w odwrotnym kierunku. Gdy LED przewodzi normalnie — dioda D jest spolaryzowana zaporowo (nie przewodzi). Gdy filtr HP generuje ujemny spike — dioda D przewodzi i klampuje do −0.7V.

- [ ] **Krok 7: Połącz pin2(LED−) OC1 i OC2 do GND_mod rail**

  Krótki drut od pin2 obu chipów do szyny GND_mod.

- [ ] **Krok 8: Połącz pin3(E) OC1 i OC2 do GND_ped rail**

  Krótki drut od pin3 obu chipów do szyny GND_ped.

- [ ] **Krok 9: Wyprowadź drut od pin4(C) OC1 i OC2 — zostaw jako wolne końce**

  Oba kolektory połącz razem (drut między nimi) i wyprowadź jeden wspólny drut ~15 cm → to będzie tap_pin. Oznacz czerwonym.

- [ ] **Krok 10: Wyprowadź drut od GND_ped rail**

  Drut ~15 cm → to będzie GND_ped pedału. Oznacz czarnym.

- [ ] **Krok 11: Wyprowadź drut od node_AB**

  Wejście od przełącznika SELECT (common). Drut ~10 cm, oznacz żółty.

- [ ] **Krok 12: Wyprowadź drut od wejścia C2 (przed kondensatorem)**

  Wejście z CV_C jack. Drut ~10 cm, oznacz niebieski.

- [ ] **Krok 13: Wyprowadź drut od GND_mod rail**

  To jest masa dla sleeve wszystkich jacków. Drut ~10 cm, oznacz zielony.

- [ ] **✓ Checkpoint 3: Test wizualny**

  Sprawdź pod lupą każde połączenie lutownicze: brak mostków, brak zimnych spoin. Sprawdź że szyna GND_mod i GND_ped nie są połączone ze sobą.

---

## Zadanie 4: Test elektryczny perfboardu (przed instalacją w pedale)

- [ ] **Krok 1: Test separacji GND_mod i GND_ped**

  Multimetr w trybie ciągłości. Sonda na GND_mod rail, sonda na GND_ped rail → BRAK sygnału dźwiękowego ✓ (szyny są odizolowane)

- [ ] **Krok 2: Test LED w PC817**

  Podaj +5V przez rezystor 470Ω na pin1 OC1, minus na pin2 (GND_mod). LED powinna zaświecić (słabo widoczne w ciemności, ewentualnie sprawdź przez kamerę telefonu — podczerwień jest widoczna). ✓

- [ ] **Krok 3: Test przełączenia fototranzystora**

  Zasilaj LED OC1 jak w Kroku 2 (prąd przez LED).
  Podłącz: + zasilacza 5V przez rezystor 10kΩ do pin4(C) OC1, minus do pin3(E) (GND_ped).
  Zmierz napięcie na pin4(C): powinno spaść do <0.5V (fototranzystor otwarty) ✓

  Odłącz zasilanie LED → napięcie na pin4(C) wraca do ~5V ✓

  Powtórz dla OC2.

- [ ] **Krok 4: Test filtra HP**

  Podaj stały +5V na wejście C1 (przez wejście SELECT common, żółty drut). Zmierz napięcie na node_AB:
  - Bezpośrednio po podaniu: ~5V → opada do 0V w ciągu ~1ms (τ = RC = 10k × 0.1µF = 1ms) ✓
  - Po ~5ms: napięcie na node_AB ≈ 0V (kondensator naładowany, filtr blokuje DC) ✓

- [ ] **✓ Checkpoint 4:** Oba optoizolatory przełączają poprawnie. Filtr HP działa. Separacja GND potwierdzona.

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
  - GND_ped pad: przylutuj czarny drut ~15 cm

  Użyj minimum cyny. Nie ruszaj sąsiednich komponentów.

- [ ] **Krok 2: Zmontuj gniazda 3.5mm w otworach**

  Przykręć Thonkiconn / Cliff przez obudowę. Przylutuj:
  - Jack A tip → do lewego terminala SELECT switch
  - Jack B tip → do prawego terminala SELECT switch
  - Jack C tip → do wejścia C2 na perfboardzie (niebieski drut)
  - Wszystkie sleeve (masa jacka) → zielony drut → GND_mod rail perfboardu

- [ ] **Krok 3: Zmontuj przełącznik SELECT (3-poz ON/OFF/ON)**

  SPDT center-off. Podłącz:
  - Lewy terminal: CV_A (tip jacka A)
  - Prawy terminal: CV_B (tip jacka B)
  - Środkowy (common): żółty drut → node_AB input perfboardu

- [ ] **Krok 4: Zmontuj przełącznik HP (2-poz ON/OFF)**

  SPST. Podłącz równolegle do C1:
  - Terminal 1: wejście C1 (od SELECT common, żółty drut)
  - Terminal 2: node_AB (za kondensatorem, po stronie R1/R2)
  - Gdy zwarty: bypass filtra HP ✓

- [ ] **Krok 5: Zmontuj przełącznik REC (2-poz ON/OFF)**

  SPST. Podłącz bezpośrednio:
  - Terminal 1: czerwony drut od tap_pin SMMH
  - Terminal 2: czarny drut GND_ped SMMH

- [ ] **Krok 6: Podłącz perfboard do pedału**

  - Czerwony drut (pin4 C OC1+OC2, kolektory) → tap_pin SMMH
  - Czarny drut (GND_ped rail) → GND_ped SMMH
  - Zielony drut (GND_mod rail) → sleeve jacków 3.5mm **TYLKO** — NIE do GND pedału

- [ ] **Krok 7: Przymocuj perfboard wewnątrz obudowy**

  Klej termiczny lub dystansowniki M3. Upewnij się że perfboard nie dotyka PCB SMMH.

- [ ] **✓ Checkpoint 6:** SMMH złożony, wszystkie połączenia wykonane. GND_mod i GND_ped nie są nigdzie połączone ze sobą.

---

## Zadanie 7: Test funkcjonalny SMMH

- [ ] **Krok 1: Test REC switch**

  Zamknij SMMH (lub trzymaj otwarty ostrożnie). Podłącz zasilanie.
  Włącz przełącznik REC → SMMH powinien wejść w tryb loopera (przytrzymanie tap). ✓
  Wyłącz REC → powrót do normalnej pracy. ✓

- [ ] **Krok 2: Test ręczny wejścia CV**

  Użyj kawałka drutu: zewrzyj tip jacka C do sleeve (symulacja triggera).
  Podaj kilka krótkich zwarć (1 per sekunda) → SMMH powinien traktować je jako tap tempo. ✓
  Sprawdź też wejścia A i B przez przełącznik SELECT.

- [ ] **Krok 3: Test z modulare (jeśli dostępny)**

  Podłącz kabel patch z outputu gate/trigger modularze do jacka C.
  Ustaw SMMH w tryb delay. Wyślij regularny trigger (np. z sekwencera lub LFO).
  Delay powinien zsynchronizować się z tempem triggera. ✓

- [ ] **Krok 4: Test filtra HP**

  Podaj stały gate (ciągłe +5V) na wejście C. SMMH nie powinien wejść w tryb loopera (filtr HP blokuje DC). ✓
  Podaj krótkie pulsy (<10ms) → normalnie triggeruje tap. ✓

- [ ] **Krok 5: Test izolacji (sprawdzenie braku humu)**

  Podłącz SMMH do wzmacniacza. Podłącz modular przez jack C. Sprawdź czy nie pojawia się hum ani brzęczenie przy podłączonym modularie — izolacja galwaniczna PC817 powinna eliminować pętle masy. ✓

- [ ] **✓ Checkpoint 7:** SMMH działa poprawnie, brak humu. Zamknij obudowę.

---

## Zadanie 8: Instalacja i test w Cathedral

Identyczny przebieg jak Zadania 6–7, tylko dla Cathedral.

- [ ] **Krok 1: Przylutuj przewody do padów tap Cathedral** (jak Krok 1 z Zadania 6)
- [ ] **Krok 2: Zmontuj gniazda 3.5mm** (jak Krok 2)
- [ ] **Krok 3: Zmontuj SELECT switch** (jak Krok 3)
- [ ] **Krok 4: Zmontuj HP switch** (jak Krok 4)
- [ ] **Krok 5: Zmontuj REC switch** (jak Krok 5)
- [ ] **Krok 6: Podłącz perfboard** (jak Krok 6 — pamiętaj o separacji GND_mod / GND_ped)
- [ ] **Krok 7: Przymocuj perfboard** (jak Krok 7)
- [ ] **Krok 8: Test REC, test ręczny wejść A/B/C, test izolacji** (jak Zadanie 7, kroki 1–5)

  **Dodatkowa uwaga dla Cathedral:** podczas tapowania reverb krótko się urywa — to normalne zachowanie firmware Cathedral, nie błąd moda.

- [ ] **✓ Checkpoint 8:** Cathedral działa poprawnie, brak humu. Zamknij obudowę.

---

## Znane ryzyka i troubleshooting

| Objaw | Możliwa przyczyna | Rozwiązanie |
|---|---|---|
| Tap w ogóle nie działa z CV | Błędna identyfikacja tap_pin/GND | Zamierz ponownie z zasilaniem; sprawdź czy tap_pin i GND_ped nie są zamienione |
| Tap nie działa — LED świeci | GND_mod i GND_ped niepołączone do pedału | Sprawdź czarny drut (GND_ped rail → GND pedału) |
| Pedał wchodzi w tryb loop przy długich gate'ach | Filtr HP nie skraca gate | Sprawdź C1 (czy filmowy, nie elektrolityczny); sprawdź node_AB |
| Trigger działa tylko raz | Kondensator nie zdążył się rozładować | Zwiększ rezystor shunt do 47kΩ (dłuższy czas rozładowania) |
| Hum mimo PC817 | GND_mod i GND_ped przypadkowo połączone | Sprawdź czy sleeve jacków nie jest podłączony do GND_ped |
| SELECT switch nie przełącza | Błędne podłączenie terminali SPDT | Zamierz ciągłość między common a lewym/prawym terminalem |

---

## Źródła i referencje

- [spec.md](spec.md) — pełna specyfikacja projektu
- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
