# CV Tap Tempo Mod — EHX SMMH + Cathedral — Instrukcja budowy (v3)

> To projekt sprzętowy. Każdy etap kończy się pomiarem multimetrem lub oscyloskopem i **punktem przerwy** — możesz odłożyć pracę po każdym z nich.
> Źródło prawdy dla wartości i połączeń: [spec.md](spec.md). Jeśli coś tu nie zgadza się ze spec.md — wygrywa spec.md.

**Cel:** zainstalować w obu pedałach obwód CV tap tempo (wejścia A/B/C, przełączniki SELECT, GATE/TRIG, REC).

**Sprzęt:** multimetr z testem diod, lutownica, oscyloskop, zasilacz USB 5V (lub bateria 9V), rezystor 1kΩ i 10kΩ do testów, kabelki z krokodylkami.

**Ważne zasady:**
- Na perfboardzie są dwie masy: **GND_mod** (modular) i **GND_ped** (pedał). Nigdy ich nie łącz.
- Diody: **pasek na obudowie = katoda**.
- PC817: **kropka lub wcięcie = pin 1**. Piny liczone przeciwnie do ruchu wskazówek zegara: 1 (lewy górny), 2 (lewy dolny), 3 (prawy dolny), 4 (prawy górny).

---

## Zadanie 1: Pomiar padów tap w obu pedałach

**Dlaczego najpierw:** od tego zależy cały mod — jeśli pad tap nie siedzi na ~3.3V lub wciśnięcie nie zwiera go do GND, zatrzymaj się i opisz wynik zanim cokolwiek kupisz.

### SMMH

- [ ] **Krok 1: Otwórz SMMH**

  Odkręć śruby na spodzie obudowy. Płytka jest przymocowana do potencjometrów — wyciągaj ostrożnie, nie ciągnij za przewody.

- [ ] **Krok 2: Zlokalizuj przycisk TAP**

  Przycisk TAP to przełącznik chwilowy podłączony do footswitcha TAP/RECORD na obudowie. Znajdź jego dwa pady lutownicze na PCB (albo miejsca, gdzie dolutowane są do niego przewody).

- [ ] **Krok 3: Zmierz napięcie na padach tap**

  Podłącz zasilanie pedału. Multimetr na DC 20V. Czarna sonda na GND pedału (np. tuleja gniazda audio). Czerwona sonda po kolei na oba pady przycisku tap.

  Oczekiwany wynik:
  - jeden pad: ~3.3V — to jest **tap_pin** (pin MCU)
  - drugi pad: 0V — to jest **GND_ped**

  Wciśnij TAP i trzymaj: tap_pin spada do ~0V ✓

  Sfotografuj i zaznacz markerem, który pad to tap_pin, a który GND_ped.

- [ ] **Krok 4: Odłącz zasilanie i zamknij SMMH tymczasowo**

### Cathedral

- [ ] **Krok 5: Otwórz Cathedral**

  Odkręć śruby na spodzie obudowy. Wyciągaj płytkę ostrożnie, nie ciągnij za przewody.

- [ ] **Krok 6: Zlokalizuj przycisk TAP**

  Znajdź pady footswitcha TAP/INFINITE na PCB (albo miejsca, gdzie dolutowane są do niego przewody).

- [ ] **Krok 7: Zmierz napięcie na padach tap**

  Podłącz zasilanie pedału. Multimetr na DC 20V. Czarna sonda na GND pedału (np. tuleja gniazda audio). Czerwona sonda po kolei na oba pady.

  Oczekiwany wynik: jeden pad ~3.3V (**tap_pin**), drugi 0V (**GND_ped**). Wciśnij TAP i trzymaj: tap_pin spada do ~0V ✓

  Sfotografuj i zaznacz markerem.

- [ ] **Krok 8: Odłącz zasilanie i zamknij Cathedral tymczasowo**

- [ ] **✓ Punkt przerwy 1:** W obu pedałach znasz tap_pin (~3.3V, spada do ~0V przy wciśnięciu) i GND_ped. Wyniki i zdjęcia zapisane. Jeśli którykolwiek pedał zachowuje się inaczej — STOP, nie kupuj elementów.

---

## Zadanie 2: Zakupy i sprawdzenie elementów

- [ ] **Krok 1: Kup elementy (lista na dwa pedały)**

| Element | Specyfikacja (pilnuj obudowy!) | Ilość |
|---|---|---|
| Optoizolator | PC817, **DIP-4** (nie PC817S, nie SMD) | 4 + 1 zapas |
| Tranzystor NPN | **BC547B**, TO-92 | 4 + 1 zapas |
| Dioda | 1N4148, **DO-35** (szklana, przewlekana) | 8 + 2 zapas |
| Rezystor | 470Ω, **0,6 W**, metalizowany | 4 |
| Rezystor | 47kΩ, 0,6 W lub 1/4 W, metalizowany | 4 |
| Rezystor | 100kΩ, 0,6 W lub 1/4 W, metalizowany | 4 |
| Kondensator filmowy | 0.22µF, 63V+, radialny, raster 5 mm | 4 |
| Kondensator filmowy (zapas) | 0.33µF, 63V+, radialny, raster 5 mm | 4 |
| Przełącznik toggle | ON/OFF/ON, SPDT, mini, gwint 6 mm | 2 |
| Przełącznik toggle | ON/OFF, SPST, mini, gwint 6 mm | 4 |
| Gniazdo 3.5mm mono | Thonkiconn PJ398SM (plastikowy gwint — izolowany od obudowy) | 6 |
| Perfboard | **5×7 cm**, raster 2.54 mm | 2 |
| Rezystory do testów | 1kΩ i 10kΩ | po 1 |
| Drut | 0.3 mm izolowany, kilka kolorów; goły drut srebrzony na szyny | 1 zestaw |

  Wszystkie elementy są przewlekane (THT). Jeśli sklep pokazuje wersję w obudowie innej niż w tabeli — to nie ten element.

- [ ] **Krok 2: Sprawdź każdy PC817**

  Multimetr w trybie diodowym (symbol diody). Trzymaj chip kropką/wcięciem w lewym górnym rogu: pin 1 lewy górny, pin 2 lewy dolny, pin 3 prawy dolny, pin 4 prawy górny.
  - czerwona na pin 1, czarna na pin 2 → **1.0–1.3V** ✓ (dioda LED)
  - odwrotnie → **OL** ✓
  - czerwona na pin 4, czarna na pin 3 → **OL** ✓ (fototranzystor wyłączony)

  Inny wynik → chip uszkodzony, odłóż.

- [ ] **Krok 3: Sprawdź diody 1N4148**
  Tryb diodowy. Czerwona sonda na końcu **bez paska** (anoda), czarna na pasku (katoda) → 0.5–0.7V ✓. Odwrotnie → OL ✓.

- [ ] **Krok 4: Zidentyfikuj nóżki każdego BC547B (przed lutowaniem!)**
  Pinout różni się między producentami — nie ufaj rysunkom z internetu, zmierz.
  Tryb diodowy. Szukasz nóżki, z której **czerwona** sonda przewodzi do **obu** pozostałych:
  - czerwona na tej nóżce, czarna na każdej z dwóch pozostałych → ~0.6–0.75V w obu przypadkach ✓ → to **baza (B)**
  - z dwóch pozostałych: ta z **nieco wyższym** odczytem (o kilka–kilkanaście mV) to **emiter (E)**, druga to **kolektor (C)**
  - każde inne ustawienie sond → OL
  Zapisz wynik na kawałku taśmy przyklejonym do tranzystora (np. „E B C” patrząc na płaską stronę).
  Jeśli żadna nóżka nie przewodzi do obu pozostałych → tranzystor PNP lub uszkodzony — odłóż.

- [ ] **✓ Punkt przerwy 2:** Wszystkie elementy na stole, PC817 i diody sprawdzone, nóżki każdego BC547B opisane.

---

## Zadanie 3: Budowa perfboardu

Budujesz dwa identyczne perfboardy (jeden na pedał). Na każdym są dwa tory: **A/B** (górny) i **C** (dolny). Oba tory są identyczne — różnią się tylko tym, skąd przychodzi sygnał.

**Sugerowane rozmieszczenie** (perfboard 5×7 cm, widok od strony elementów). Obowiązuje **lista połączeń** niżej — rozmieszczenie możesz zmienić, połączeń nie.

    ┌──────────────────────────────── 7 cm ────────────────────────────────┐
    │ ═══ szyna GND_mod (goły drut) ═══════════════════════   ┊           ║ │
    │                                                         ┊           ║ │
    │  in_AB  [C1]  [R1↕] [R5]  [D3]  [Q1]   [R2 470Ω]  [D1] [OC1]        ║ │
    │                                                         ┊           ║ │
    │  in_C   [C2]  [R3↕] [R6]  [D4]  [Q2]   [R4 470Ω]  [D2] [OC2]        ║ │
    │                                                         ┊     GND_ped║ │
    │ ═══ szyna GND_mod ═══════════════════════════════════   ┊   (szyna) ║ │
    └──────────────────────────────────────────────────────────────────────┘
      strona modulara (lewo)                    ┊ OC: piny 1-2 w lewo, 3-4 w prawo
                                                ┊ ≥ 4 puste kolumny między GND_mod a GND_ped

**Lista połączeń toru A/B** (zgodna z tabelą „Połączenia toru” w spec.md):

| Węzeł | Co lutujesz razem | Uwagi |
|---|---|---|
| in_AB | drut od SELECT (common), jedna nóżka R2, jedna nóżka C1, drut do GATE/TRIG | |
| LED+ | druga nóżka R2, pin 1 OC1, **katoda** D1 (pasek) | |
| LED− | pin 2 OC1, **anoda** D1 (bez paska), **kolektor** Q1 | |
| node_h | druga nóżka C1, jedna nóżka R1, jedna nóżka R5, drugi drut do GATE/TRIG | |
| baza | druga nóżka R5, **baza** Q1, **katoda** D3 (pasek) | |
| GND_mod | **emiter** Q1, druga nóżka R1, **anoda** D3 (bez paska) | szyna GND_mod |
| tap_pin | pin 4 OC1 i pin 4 OC2 (połączone), czerwony drut ~15 cm | strona pedału |
| GND_ped | pin 3 OC1 i pin 3 OC2, czarny drut ~15 cm | szyna GND_ped |

**Lista połączeń toru C:**

| Węzeł | Co lutujesz razem | Uwagi |
|---|---|---|
| in_C | drut od tip jacka C, jedna nóżka R4, jedna nóżka C2 | bez GATE/TRIG — tor C zawsze TRIG |
| LED+ (C) | druga nóżka R4, pin 1 OC2, **katoda** D2 (pasek) | |
| LED− (C) | pin 2 OC2, **anoda** D2 (bez paska), **kolektor** Q2 | |
| node_h (C) | druga nóżka C2, jedna nóżka R3, jedna nóżka R6 | |
| baza (C) | druga nóżka R6, **baza** Q2, **katoda** D4 (pasek) | |
| GND_mod | **emiter** Q2, druga nóżka R3, **anoda** D4 (bez paska) | szyna GND_mod |

Elementy: R1, R3 = 100kΩ · R5, R6 = 47kΩ · R2, R4 = 470Ω 0,6 W · C1, C2 = 0.22µF · D1–D4 = 1N4148 · Q1, Q2 = BC547B · OC1, OC2 = PC817.

- [ ] **Krok 1: Przygotuj perfboard**

  Perfboard 5×7 cm. Markerem zaznacz: szynę GND_mod (górna i dolna krawędź, strona lewa), szynę GND_ped (prawa krawędź) i pustą strefę ≥ 4 kolumn między nimi. Podpisz szyny.

- [ ] **Krok 2: Przylutuj szyny**

  Gołym drutem zrób szynę GND_mod (góra i dół, połączone ze sobą krótkim drutem po lewej) i osobno szynę GND_ped (prawa krawędź). Multimetr w trybie ciągłości: GND_mod ↔ GND_ped → **brak sygnału** ✓.

- [ ] **Krok 3: Wlutuj OC1 i OC2 (PC817)**

  Kropka (pin 1) w lewym górnym rogu: piny 1–2 po stronie modulara, piny 3–4 po stronie pedału, przy pustej strefie. Max 3 sekundy na nóżkę.

- [ ] **Krok 4: Wlutuj R2, R4 (470Ω 0,6 W) i diody D1, D2**

  R2: jedna nóżka w węźle in_AB, druga przy pin 1 OC1. D1 **równolegle do LED, odwrotnie**: **pasek (katoda) do pin 1**, drugi koniec (anoda) do pin 2. To samo w torze C: R4, D2, OC2.

- [ ] **Test diod przy PC817 (zaraz po wlutowaniu D1/D2!)**
  Tryb diodowy, pomiar między pin 1 a pin 2 każdego PC817:
  - czerwona na pin 1, czarna na pin 2 → **1.0–1.3V** ✓ (przewodzi LED)
  - czerwona na pin 2, czarna na pin 1 → **0.5–0.7V** ✓ (przewodzi D1, antyparalel)
  ❌ Jeśli w pierwszym pomiarze widzisz 0.5–0.7V, a w drugim OL — **dioda D1 jest odwrotnie**. Mod nie zadziała. Wylutuj i odwróć.

- [ ] **Krok 5: Wlutuj Q1 i Q2 (BC547B)**

  Według opisu nóżek z taśmy (Zadanie 2, Krok 4). **Kolektor** do pin 2 OC (węzeł LED−), **emiter** do szyny GND_mod, **baza** zostaje na razie wolna (połączysz w Kroku 7). Nie przegrzewaj — max 3 sekundy na nóżkę.

- [ ] **Krok 6: Wlutuj D3 i D4 (klamp bazy)**

  **Pasek (katoda) do bazy** Q1 / Q2, drugi koniec (anoda) do szyny GND_mod.

  Sprawdź: tryb diodowy, czerwona na GND_mod, czarna na bazie Q1 → **0.5–0.7V** ✓ (przewodzi D3).
  ❌ **OL** → D3 jest odwrotnie (pasek musi być przy bazie). Wylutuj i odwróć.
  (Pomiar w drugą stronę nic nie rozstrzyga — przewodzi wtedy złącze baza-emiter tranzystora.)

- [ ] **Krok 7: Wlutuj R5, R6 (47kΩ), R1, R3 (100kΩ) i C1, C2 (0.22µF)**

  R5: baza Q1 ↔ node_h. R1: node_h ↔ GND_mod. C1: in_AB ↔ node_h (kondensator filmowy — orientacja dowolna). W torze C analogicznie: R6, R3, C2 (C2 między in_C a node_h toru C).

- [ ] **Krok 8: Dokończ połączenia według obu tabel**

  Odhacz ołówkiem w tabelach każdy wiersz po zlutowaniu. Kolektory OC (pin 4 OC1 i pin 4 OC2) połącz krótkim drutem. Piny 3 OC1 i OC2 do szyny GND_ped.

- [ ] **Krok 9: Wyprowadź druty**

  | Drut | Skąd | Dokąd (później) | Kolor |
  |---|---|---|---|
  | tap_pin | pin 4 OC1/OC2 | pad tap_pin pedału | czerwony, ~15 cm |
  | GND_ped | szyna GND_ped | pad GND_ped pedału | czarny, ~15 cm |
  | GND_mod | szyna GND_mod | sleeve wszystkich jacków | zielony, ~10 cm |
  | in_AB | węzeł in_AB | SELECT (common, środkowy) | żółty, ~10 cm |
  | in_C | węzeł in_C | tip jacka C | niebieski, ~10 cm |
  | GATE/TRIG ×2 | in_AB i node_h toru A/B | dwa terminale GATE/TRIG | biały, 2× ~10 cm |

- [ ] **✓ Punkt przerwy 3:** Oba tory zlutowane, test diod przy PC817 OK, pod lupą brak mostków. Szyny GND_mod i GND_ped nie są połączone.

---

## Zadanie 4: Test perfboardu na stole

Na czas testu możesz użyć jednego zasilacza 5V dla obu stron — izolację sprawdzasz osobno w Kroku 1.

- [ ] **Krok 1: Separacja mas** — tryb ciągłości: GND_mod ↔ GND_ped → brak sygnału ✓.
- [ ] **Krok 2: Tryb GATE (stały sygnał)** — zewrzyj C1 kawałkiem drutu (udaje GATE/TRIG w pozycji GATE). Podaj +5V na in_AB, minus na GND_mod. Multimetr w trybie diodowym: czerwona na pin 4 OC1, czarna na pin 3 → **< 0.4V** ✓ (fototranzystor przewodzi), tak długo jak podajesz 5V. Odłącz 5V → **OL** ✓. Usuń zworkę z C1.
- [ ] **Krok 3: Tryb TRIG (impuls) — oscyloskop** — zasil stronę pedału: +5V przez rezystor 10kΩ do pin 4 OC1, minus do pin 3 (GND_ped). Sonda oscyloskopu na pin 4. Podaj +5V na in_AB na ~1 s (dotknięcie kabelkiem) → na pin 4 napięcie spada do ~0V na **~15–135 ms**, potem wraca do 5V, mimo że wejście nadal ma 5V ✓. Zapisz zmierzony czas.
- [ ] **Krok 4: Powtórz Kroki 2–3 dla toru C** (in_C, OC2). W Kroku 2 zwieraj C2.
- [ ] **Krok 5: Odporność na ±10V** (jeśli masz moduł 20 Vpp) — podaj na in_AB sygnał prostokątny ±10V (np. LFO square) przez 10 s. Nic nie powinno się nagrzewać do stopnia, w którym nie da się dotknąć; R2 może być lekko ciepły ✓. Powtórz Krok 3 — wynik bez zmian ✓.

- [ ] **✓ Punkt przerwy 4:** Oba tory przełączają w trybie GATE i dają impuls w trybie TRIG. Masy rozdzielone.

---

## Zadanie 5: Wiercenie obudowy

Wykonaj dla każdego pedału osobno. Zacznij od SMMH.

- [ ] **Krok 1: Zaplanuj rozmieszczenie otworów**

  Narysuj ołówkiem / na taśmie malarskiej:
  - 3× otwór na gniazda 3.5mm (średnica wg PJ398SM — sprawdź suwmiarką gwint gniazda)
  - 3× otwór 6 mm na przełączniki toggle (SELECT, GATE/TRIG, REC)

  Sprawdź, czy otwory nie kolidują z elementami w środku (zmierz od krawędzi obudowy do elementów na PCB).

- [ ] **Krok 2: Wywierć otwory pilotażowe 2 mm**

- [ ] **Krok 3: Rozwierć do docelowej średnicy**

  Stopniowo: 2 mm → 4 mm → docelowa średnica. Usuń zadziory pilnikiem.

- [ ] **Krok 4: Przymierz gniazda i przełączniki**

  Wsuń bez przykręcania. Sprawdź, czy pasują i nie dotykają PCB pedału.

- [ ] **✓ Punkt przerwy 5:** Otwory wywiercone, elementy pasują. To samo dla Cathedral.

---

## Zadanie 6: Instalacja w SMMH

- [ ] **Krok 1: Przylutuj przewody do padów tap SMMH**

  Na padach zaznaczonych w Zadaniu 1: czerwony drut do tap_pin, czarny do GND_ped. Minimum cyny, nie ruszaj sąsiednich elementów.

- [ ] **Krok 2: Zamontuj gniazda 3.5mm**

  Przykręć PJ398SM. Przylutuj:
  - tip jacka A → lewy terminal SELECT
  - tip jacka B → prawy terminal SELECT
  - tip jacka C → niebieski drut (in_C)
  - sleeve wszystkich trzech jacków → zielony drut (GND_mod)

- [ ] **Krok 3: Zamontuj SELECT (ON/OFF/ON)**

  Środkowy terminal (common) → żółty drut (in_AB). Lewy → jack A, prawy → jack B.

- [ ] **Krok 4: Zamontuj GATE/TRIG (ON/OFF)**

  Dwa białe druty (in_AB i node_h) do dwóch terminali przełącznika. Przełącznik w pozycji ON zwiera C1 → **GATE**; OFF → **TRIG**. Opisz obudowę: GATE u góry, TRIG na dole (zgodnie z kierunkiem dźwigni dla pozycji ON / OFF).

- [ ] **Krok 5: Zamontuj REC (ON/OFF)**

  Terminal 1 → pad tap_pin SMMH (lub czerwony drut), terminal 2 → pad GND_ped SMMH (lub czarny drut).

- [ ] **Krok 6: Podłącz perfboard**

  - czerwony (tap_pin) → pad tap_pin SMMH
  - czarny (GND_ped) → pad GND_ped SMMH
  - zielony (GND_mod) → sleeve jacków **TYLKO** — nigdy do GND pedału ani do obudowy

- [ ] **Krok 7: Przymocuj perfboard**

  Taśma dwustronna piankowa lub klej na gorąco. Perfboard nie może dotykać PCB pedału ani metalowej obudowy (podłóż izolację, np. kawałek kaptonu).

- [ ] **Krok 8: Kontrola izolacji w obudowie**
  Tryb ciągłości: GND_mod (sleeve dowolnego jacka CV) ↔ metalowa obudowa pedału → brak sygnału ✓.
  Tip każdego jacka CV ↔ obudowa → brak sygnału ✓.
  Jeśli piszczy — coś ze strony modulara dotyka obudowy (najczęściej gniazdo lub drut przy otworze). Znajdź i odizoluj.

- [ ] **✓ Punkt przerwy 6:** SMMH złożony, wszystkie połączenia wykonane, izolacja potwierdzona.

---

## Zadanie 7: Testy funkcjonalne SMMH

- [ ] **Krok 1: REC** — włącz REC na ~1 s → SMMH nagrywa pętlę (≥ 0,5 s przytrzymania). Wyłącz → pętla gra ✓.
- [ ] **Krok 2: Test ręczny wejścia C** — +5V przez rezystor 1kΩ na tip jacka C, minus na sleeve. Dotknij i puść kilka razy w równym tempie (~1 na sekundę) → SMMH ustawia czas delay ✓. **Nie** zwieraj tip ze sleeve — to nic nie da (strona modulara nie ma zasilania).
- [ ] **Krok 3: Wejścia A i B** — +5V przez rezystor 1kΩ na tip jacka A, minus na sleeve, SELECT na A, GATE/TRIG na TRIG. Dotknij i puść kilka razy w równym tempie → SMMH ustawia czas delay ✓. Powtórz dla jacka B z SELECT na B ✓.
- [ ] **Krok 4: Minimalny impuls (najważniejszy pomiar!)** — sekwencer z regulowaną długością gate → wejście A, GATE/TRIG na **GATE**. Zacznij od gate 50 ms i skracaj (50 → 20 → 10 → 5 → 2 → 1 ms). Zapisz najkrótszy gate, który SMMH jeszcze łapie jako tap. Jeśli oscyloskopem możesz zmierzyć długość gate — zmierz.
  - wynik ≤ 10 ms → OK, zostaje 0.22µF ✓
  - wynik > 10 ms → wymień C1 i C2 na **0.33µF** (zapas z zakupów) i powtórz Krok 5
  Wynik dopisz do spec.md, sekcja „Wymagania czasowe pedałów”.
- [ ] **Krok 5: Próg przytrzymania** — GATE/TRIG na **TRIG**, gate 3 s na wejście A → SMMH robi **jeden tap**, nie nagrywa pętli ✓. To samo na wejściu C ✓. Przełącz na **GATE** → gate 3 s nagrywa pętlę ✓ (zgodnie z zamierzeniem).
- [ ] **Krok 6: Tempo z sekwencera** — zegar 120 BPM (gate 50%) na wejście C → delay synchronizuje się z tempem ✓. Powtórz z gate 90% przy 300 BPM → każdy krok łapany ✓.
- [ ] **Krok 7: Brak humu** — SMMH do wzmacniacza, modular podłączony do jacka C, cisza na wejściu gitary → brak humu i brzęczenia ✓.

- [ ] **✓ Punkt przerwy 7:** SMMH działa, minimalny impuls zapisany. Zamknij obudowę.

---

## Zadanie 8: Instalacja i testy Cathedral

### Instalacja

- [ ] **Krok 1: Przylutuj przewody do padów tap Cathedral**

  Na padach zaznaczonych w Zadaniu 1: czerwony drut do tap_pin, czarny do GND_ped. Minimum cyny, nie ruszaj sąsiednich elementów.

- [ ] **Krok 2: Zamontuj gniazda 3.5mm**

  Przykręć PJ398SM. Przylutuj: tip A → lewy terminal SELECT, tip B → prawy terminal SELECT, tip C → niebieski drut (in_C), sleeve wszystkich trzech → zielony drut (GND_mod).

- [ ] **Krok 3: Zamontuj SELECT (ON/OFF/ON)**

  Środkowy terminal (common) → żółty drut (in_AB). Lewy → jack A, prawy → jack B.

- [ ] **Krok 4: Zamontuj GATE/TRIG (ON/OFF)**

  Dwa białe druty (in_AB i node_h) do dwóch terminali. ON = **GATE**, OFF = **TRIG**. Opisz obudowę: GATE u góry, TRIG na dole.

- [ ] **Krok 5: Zamontuj REC (ON/OFF)**

  Terminal 1 → pad tap_pin Cathedral, terminal 2 → pad GND_ped Cathedral.

- [ ] **Krok 6: Podłącz perfboard**

  Czerwony → tap_pin Cathedral, czarny → GND_ped Cathedral, zielony (GND_mod) → sleeve jacków **TYLKO**.

- [ ] **Krok 7: Przymocuj perfboard**

  Taśma dwustronna piankowa lub klej na gorąco, z izolacją od PCB i obudowy.

- [ ] **Krok 8: Kontrola izolacji w obudowie**
  Tryb ciągłości: GND_mod (sleeve dowolnego jacka CV) ↔ metalowa obudowa → brak sygnału ✓. Tip każdego jacka CV ↔ obudowa → brak sygnału ✓. Jeśli piszczy — znajdź i odizoluj.

### Testy

- [ ] **Krok 9: REC** — włącz REC na ~1 s (> 350 ms) → **infinite reverb** (wybrzmienie się nie wycisza) ✓. Wyłącz → normalna praca ✓. (W trybie ECHO infinite nie działa — test w innym trybie.)
- [ ] **Krok 10: Test ręczny wejścia C** — +5V przez rezystor 1kΩ na tip jacka C, minus na sleeve. Dotknij i puść kilka razy w równym tempie → Cathedral ustawia pre-delay ✓. **Nie** zwieraj tip ze sleeve.
- [ ] **Krok 11: Wejścia A i B** — jak Krok 10, na jacku A (SELECT na A, GATE/TRIG na TRIG), potem na jacku B (SELECT na B) ✓.
- [ ] **Krok 12: Minimalny impuls** — sekwencer z regulowaną długością gate → wejście A, GATE/TRIG na **GATE**. Skracaj gate 50 → 20 → 10 → 5 → 2 → 1 ms. Zapisz najkrótszy gate rozpoznawany jako tap.
  - wynik ≤ 10 ms → OK ✓
  - wynik > 10 ms → wymień C1 i C2 w Cathedral na **0.33µF** i powtórz Krok 13
  Wynik dopisz do spec.md, sekcja „Wymagania czasowe pedałów”.
- [ ] **Krok 13: Próg przytrzymania** — GATE/TRIG na **TRIG**, gate 3 s na wejście A → **jeden tap, bez infinite** ✓. To samo na wejściu C ✓. Przełącz na **GATE** → gate 3 s włącza infinite ✓.
- [ ] **Krok 14: Tempo z sekwencera** — zegar 120 BPM (gate 50%) na wejście C → pre-delay synchronizuje się ✓.
- [ ] **Krok 15: Brak humu** — Cathedral do wzmacniacza, modular podłączony do jacka C → brak humu ✓.

  **Uwaga:** podczas tapowania reverb krótko się urywa — to zachowanie firmware Cathedral, nie błąd moda.

- [ ] **✓ Punkt przerwy 8:** Cathedral działa, minimalny impuls zapisany. Zamknij obudowę.

---

## Troubleshooting

| Objaw | Możliwa przyczyna | Co zrobić |
|---|---|---|
| Nic nie działa, test diod przy PC817: 0.5–0.7V / OL | D1/D2 odwrotnie (ten sam kierunek co LED) | Wylutuj i odwróć diodę: pasek do pin 1 |
| GATE działa, TRIG nie | Impuls za krótki dla pedału | C1/C2 → 0.33µF |
| TRIG nie działa, GATE też nie | Złe nóżki Q1/Q2 albo D3/D4 odwrotnie | Sprawdź opis nóżek z Zadania 2; pasek D3 do bazy |
| Tap nie działa w ogóle | Zamienione tap_pin i GND_ped | Zmierz ponownie pady (Zadanie 1) |
| Pedał wchodzi w looper / infinite w trybie TRIG | GATE/TRIG zwarty albo C1 zwarty | Sprawdź przełącznik i C1 |
| Hum po podłączeniu modulara | GND_mod dotyka obudowy lub GND_ped | Zadanie 6 Krok 8 |
| R2 gorący | Długi sygnał ±12V — normalne do ~0,2 W | Sprawdź, czy R2 to 0,6 W, nie 1/4 W |

---

## Źródła

- [spec.md](spec.md) — specyfikacja v3 (wartości, połączenia, symulacje)
- [EHX Stereo Memory Man with Hazarai — manual (PDF)](https://www.ehx.com/wp-content/uploads/2021/01/stereo-memory-man-with-hazarai-manual.pdf)
- [EHX Cathedral — manual (ManualsLib)](https://www.manualslib.com/manual/2900221/Electro-Harmonix-Cathedral-Stereo-Reverb.html)
- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html)
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai)
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
