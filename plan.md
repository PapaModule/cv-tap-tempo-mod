# CV Tap Tempo Mod — EHX SMMH + Cathedral — Instrukcja budowy (v3)

> To projekt sprzętowy. Każdy etap kończy się pomiarem multimetrem lub oscyloskopem i **punktem przerwy** — możesz odłożyć pracę po każdym z nich.
> Źródło prawdy dla wartości i połączeń: [spec.md](spec.md). Jeśli coś tu nie zgadza się ze spec.md — wygrywa spec.md.

**Cel:** zainstalować w obu pedałach obwód CV tap tempo (wejścia A/B/C, przełączniki SELECT, GATE/TRIG, REC).

**Sprzęt:** multimetr z testem diod, lutownica, oscyloskop, zasilacz USB 5V z przewodem do testów (moduł „USB breakout” albo przecięty kabel USB: czerwony = +5V, czarny = minus) lub bateria 9V, rezystor 1kΩ i 10kΩ do testów, kabelki z krokodylkami, kabel patch 3.5mm.

**Ważne zasady:**
- Na perfboardzie są dwie masy: **GND_mod** (modular) i **GND_ped** (pedał). W pedale nigdy ich nie łącz (jedyny wyjątek: test na stole w Zadaniu 4, Krok 3 — opisany wprost).
- Diody: **pasek na obudowie = katoda**.
- PC817: **kropka lub wcięcie = pin 1**. Piny liczone przeciwnie do ruchu wskazówek zegara: 1 (lewy górny), 2 (lewy dolny), 3 (prawy dolny), 4 (prawy górny).
- Test ciągłości: „piknięcie” = połączone, „brak piknięcia” = rozłączone.

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
| Rezystor | 100kΩ, 0,6 W lub 1/4 W, metalizowany | 8 |
| Kondensator filmowy | 0.22µF, 63V+, radialny, raster 5 mm | 4 |
| Kondensator filmowy (zapas) | 0.33µF, 63V+, radialny, raster 5 mm | 4 |
| Przełącznik toggle | ON/OFF/ON, SPDT, mini, gwint 6 mm | 2 |
| Przełącznik toggle | ON/OFF, SPST, mini, gwint 6 mm | 4 |
| Gniazdo 3.5mm mono | Thonkiconn PJ398SM (plastikowy gwint — izolowany od obudowy) | 6 |
| Perfboard | **5×7 cm**, raster 2.54 mm | 2 |
| Rezystory do testów | 1kΩ i 10kΩ | po 1 |
| Drut | 0.3 mm izolowany, kilka kolorów; goły drut srebrzony na szyny | 1 zestaw |
| Montaż | taśma dwustronna piankowa, taśma kapton, koszulka termokurczliwa | po 1 |

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
  - z dwóch pozostałych: ta z **nieco wyższym** odczytem to **emiter (E)**, druga to **kolektor (C)**. Różnica bywa tylko kilka mV — mierz uważnie, po dwa razy.
  - każde inne ustawienie sond → OL

  Jeśli multimetr ma gniazdo **hFE** (NPN): włóż tranzystor zgodnie z ustalonym E-B-C → odczyt zwykle **150–450** ✓ (multimetr mierzy przy małym prądzie, więc wynik bywa niższy niż w katalogu). Odczyt < 30 → C i E zamienione; odwróć i sprawdź ponownie.

  Zapisz wynik na kawałku taśmy przyklejonym do tranzystora (np. „E B C” patrząc na płaską stronę, nóżkami w dół).
  Jeśli żadna nóżka nie przewodzi do obu pozostałych → tranzystor PNP lub uszkodzony — odłóż.

- [ ] **✓ Punkt przerwy 2:** Wszystkie elementy na stole, PC817 i diody sprawdzone, nóżki każdego BC547B opisane.

---

## Zadanie 3: Budowa perfboardu

Budujesz dwa identyczne perfboardy (jeden na pedał). Na każdym są dwa tory: **A/B** (górny) i **C** (dolny). Oba tory są identyczne — różnią się tylko tym, skąd przychodzi sygnał.

**Sugerowane rozmieszczenie** (perfboard 5×7 cm, widok od strony elementów). Obowiązuje **lista połączeń** niżej — rozmieszczenie możesz zmienić, połączeń nie.

    ┌──────────────────────────────── 7 cm ─────────────────────────────────┐
    │ ═══ szyna GND_mod (goły drut) ════════════════════════   ┊           ║ │
    │                                                          ┊           ║ │
    │  in_AB [R7↕] [C1] [R1↕] [R5] [D3] [Q1]  [R2 470Ω] [D1] [OC1]         ║ │
    │                                                          ┊           ║ │
    │  in_C  [R8↕] [C2] [R3↕] [R6] [D4] [Q2]  [R4 470Ω] [D2] [OC2]         ║ │
    │                                                          ┊    GND_ped║ │
    │ ═══ szyna GND_mod ════════════════════════════════════   ┊   (szyna) ║ │
    └───────────────────────────────────────────────────────────────────────┘
      strona modulara (lewo)                     ┊ OC: piny 1-2 w lewo, 3-4 w prawo
                                                 ┊ ≥ 4 puste kolumny między GND_mod a GND_ped

**Lista połączeń toru A/B** (zgodna z tabelą „Połączenia toru” w spec.md):

| Węzeł | Co lutujesz razem | Uwagi |
|---|---|---|
| in_AB | drut od SELECT (common), jedna nóżka R2, jedna nóżka C1, jedna nóżka R7, drut do GATE/TRIG | |
| LED+ | druga nóżka R2, pin 1 OC1, **katoda** D1 (pasek) | |
| LED− | pin 2 OC1, **anoda** D1 (bez paska), **kolektor** Q1 | |
| node_h | druga nóżka C1, jedna nóżka R1, jedna nóżka R5, drugi drut do GATE/TRIG | |
| baza | druga nóżka R5, **baza** Q1, **katoda** D3 (pasek) | |
| GND_mod | **emiter** Q1, druga nóżka R1, druga nóżka R7, **anoda** D3 (bez paska) | szyna GND_mod; + zielony drut do sleeve wszystkich jacków |
| tap_pin | pin 4 OC1 i pin 4 OC2 (połączone), czerwony drut ~15 cm | strona pedału; + REC (Zadanie 6) |
| GND_ped | pin 3 OC1 i pin 3 OC2, czarny drut ~15 cm | szyna GND_ped; + REC (Zadanie 6) |

**Lista połączeń toru C:**

| Węzeł | Co lutujesz razem | Uwagi |
|---|---|---|
| in_C | drut od tip jacka C, jedna nóżka R4, jedna nóżka C2, jedna nóżka R8 | bez GATE/TRIG — tor C zawsze TRIG |
| LED+ (C) | druga nóżka R4, pin 1 OC2, **katoda** D2 (pasek) | |
| LED− (C) | pin 2 OC2, **anoda** D2 (bez paska), **kolektor** Q2 | |
| node_h (C) | druga nóżka C2, jedna nóżka R3, jedna nóżka R6 | |
| baza (C) | druga nóżka R6, **baza** Q2, **katoda** D4 (pasek) | |
| GND_mod | **emiter** Q2, druga nóżka R3, druga nóżka R8, **anoda** D4 (bez paska) | szyna GND_mod |

Elementy: R1, R3, R7, R8 = 100kΩ · R5, R6 = 47kΩ · R2, R4 = 470Ω 0,6 W · C1, C2 = 0.22µF · D1–D4 = 1N4148 · Q1, Q2 = BC547B · OC1, OC2 = PC817.

- [ ] **Krok 1: Przygotuj perfboard**

  Perfboard 5×7 cm. Markerem zaznacz: szynę GND_mod (górna i dolna krawędź, strona lewa), szynę GND_ped (prawa krawędź) i pustą strefę ≥ 4 kolumn między nimi. Podpisz szyny.

- [ ] **Krok 2: Przylutuj szyny**

  Gołym drutem zrób szynę GND_mod (góra i dół, połączone ze sobą krótkim drutem po lewej) i osobno szynę GND_ped (prawa krawędź). Multimetr w trybie ciągłości: GND_mod ↔ GND_ped → **brak piknięcia** ✓.

- [ ] **Krok 3: Wlutuj OC1 i OC2 (PC817)**

  Kropka (pin 1) w lewym górnym rogu: piny 1–2 po stronie modulara, piny 3–4 po stronie pedału, przy pustej strefie. Max 3 sekundy na nóżkę.

- [ ] **Krok 4: Wlutuj R2, R4 (470Ω 0,6 W) i diody D1, D2**

  R2: jedna nóżka przy pin 1 OC1, druga nóżka w miejscu węzła in_AB (pozostałe elementy węzła in_AB dołożysz w Krokach 7–8). D1 **równolegle do LED, odwrotnie**: **pasek (katoda) do pin 1**, drugi koniec (anoda) do pin 2. To samo w torze C: R4, D2, OC2.

- [ ] **Test diod przy PC817 (zaraz po wlutowaniu D1/D2!)**

  Tryb diodowy, pomiar między pin 1 a pin 2 każdego PC817:

  - czerwona na pin 1, czarna na pin 2 → **1.0–1.3V** ✓ (przewodzi LED)
  - czerwona na pin 2, czarna na pin 1 → **0.5–0.7V** ✓ (przewodzi D1, antyparalel)

  ❌ Jeśli w pierwszym pomiarze widzisz 0.5–0.7V, a w drugim OL — **dioda D1 jest odwrotnie**. Mod nie zadziała. Wylutuj i odwróć.

- [ ] **Krok 5: Wlutuj Q1 i Q2 (BC547B)**

  Według opisu nóżek z taśmy (Zadanie 2, Krok 4). **Kolektor** do pin 2 OC (węzeł LED−), **emiter** do szyny GND_mod. Bazy na razie nie łącz z niczym (D3 dołożysz w Kroku 6, R5 w Kroku 7). Nie przegrzewaj — max 3 sekundy na nóżkę.

- [ ] **Krok 6: Wlutuj D3 i D4 (klamp bazy)**

  **Pasek (katoda) do bazy** Q1 / Q2, drugi koniec (anoda) do szyny GND_mod.

  Sprawdź D3: tryb diodowy, czerwona na GND_mod, czarna na bazie Q1 → **0.5–0.7V** ✓ (przewodzi D3).
  ❌ **OL** → D3 jest odwrotnie (pasek musi być przy bazie). Wylutuj i odwróć.

  Sprawdź D4: czerwona na GND_mod, czarna na bazie Q2 → **0.5–0.7V** ✓ (przewodzi D4).
  ❌ **OL** → D4 jest odwrotnie. Wylutuj i odwróć.

  (Pomiar w drugą stronę nic nie rozstrzyga — przewodzi wtedy złącze baza-emiter tranzystora.)

- [ ] **Krok 7: Wlutuj R5, R6 (47kΩ), R1, R3, R7, R8 (100kΩ) i C1, C2 (0.22µF)**

  - R5: baza Q1 ↔ node_h. R1: node_h ↔ GND_mod. C1: in_AB ↔ node_h (kondensator filmowy — orientacja dowolna). R7: in_AB ↔ GND_mod.
  - Tor C: R6: baza Q2 ↔ node_h (C). R3: node_h (C) ↔ GND_mod. C2: in_C ↔ node_h (C). R8: in_C ↔ GND_mod.

- [ ] **Krok 8: Dokończ połączenia według obu tabel**

  Odhacz ołówkiem w tabelach każdy wiersz po zlutowaniu. Kolektory OC (pin 4 OC1 i pin 4 OC2) połącz krótkim drutem. Piny 3 OC1 i OC2 do szyny GND_ped.

- [ ] **Krok 9: Wyprowadź druty**

  | Drut | Skąd | Dokąd (później) | Kolor |
  |---|---|---|---|
  | tap_pin | pin 4 OC1/OC2 | przewód z padu tap_pin pedału | czerwony, ~15 cm |
  | GND_ped | szyna GND_ped | przewód z padu GND_ped pedału | czarny, ~15 cm |
  | GND_mod | szyna GND_mod | sleeve wszystkich jacków | zielony, ~10 cm |
  | in_AB | węzeł in_AB | SELECT (common, środkowy) | żółty, ~10 cm |
  | in_C | węzeł in_C | tip jacka C | niebieski, ~10 cm |
  | GATE/TRIG ×2 | in_AB i node_h toru A/B | dwa terminale GATE/TRIG | biały, 2× ~10 cm |

  Końce wszystkich przewodów rozsuń i zabezpiecz (np. kawałkiem taśmy) — zetknięte białe przewody działają jak włączony GATE.

- [ ] **✓ Punkt przerwy 3:** Oba tory zlutowane, test diod przy PC817 i test D3/D4 OK, pod lupą brak mostków. Szyny GND_mod i GND_ped nie są połączone.

---

## Zadanie 4: Test perfboardu na stole

- [ ] **Krok 1: Separacja mas** — tryb ciągłości: GND_mod ↔ GND_ped → **brak piknięcia** ✓.

- [ ] **Krok 2: Tryb GATE (stały sygnał)**

  Zewrzyj ze sobą końce dwóch białych przewodów GATE/TRIG (udaje pozycję GATE i od razu sprawdza te przewody). Podaj +5V na in_AB (żółty drut), minus na GND_mod (zielony drut). Multimetr w trybie diodowym: czerwona na pin 4 OC1, czarna na pin 3 → **< 0.4V** ✓ (fototranzystor przewodzi), tak długo jak podajesz 5V. Odłącz 5V → **OL** ✓. Rozsuń białe przewody.

- [ ] **Krok 3: Tryb TRIG (impuls) — oscyloskop**

  - **Masy tylko na czas tego testu:** minus zasilacza połącz z GND_mod **i** z pin 3 OC1 (GND_ped). W pedale masy nigdy nie są łączone.
  - Strona pedału: +5V przez rezystor 10kΩ do pin 4 OC1.
  - Oscyloskop: sonda na pin 4, masa sondy na minusie zasilacza. Ustawienia: 20 ms/działkę, 2 V/działkę, wyzwalanie zboczem opadającym ~2,5V, tryb SINGLE.
  - Dotknij +5V do in_AB (żółty drut) i trzymaj ~1 s, potem puść.
  - Oczekiwane: na pin 4 napięcie spada do ~0V na **~15–135 ms** (przy 5V z zasilacza zwykle 15–40 ms), potem łagodnie wraca do 5V, mimo że wejście nadal ma 5V ✓. Czas mierz na poziomie ~2,5V. Zapisz go.
  - Powtórz dotknięcie 3 razy (oscyloskop znów w SINGLE) — **każde** dotknięcie daje impuls ✓ (R7 rozładowuje C1 po puszczeniu).
  - ❌ Pin 4 spada tylko do 1–4V zamiast ~0V → zamienione C i E w Q1 (patrz Troubleshooting).

- [ ] **Krok 4: Tor C**

  Powtórz Krok 2 dla toru C: zamiast białych przewodów zewrzyj kawałkiem drutu nóżki C2; +5V na in_C (niebieski drut), minus na GND_mod; multimetr czerwona na pin 4 OC2, czarna na pin 3 → **< 0.4V** ✓; odłącz 5V → **OL** ✓. Usuń zworkę z C2.
  Powtórz Krok 3 dla toru C: pull-up 10kΩ do pin 4 OC2, sonda na pin 4 OC2, dotknięcie +5V do in_C → impuls **~15–135 ms** przy każdym z 3 dotknięć ✓.

- [ ] **Krok 5: Odporność na ±10V** (jeśli masz moduł 20 Vpp)

  Kabel z wyjścia modułu: tip → in_AB, sleeve (masa modułu) → GND_mod. Sygnał prostokątny ±10V (np. LFO square) ~1–2 Hz przez 10 s, oscyloskop na pin 4 OC1 jak w Kroku 3 (tryb ciągły zamiast SINGLE): krótki impuls przy każdym zboczu narastającym, a nie stałe 0V przez całą dodatnią połówkę ✓. Nic nie nagrzewa się tak, że nie da się dotknąć; R2 może być lekko ciepły ✓. To samo dla toru C (tip → in_C, pin 4 OC2) ✓.

- [ ] **✓ Punkt przerwy 4:** Oba tory przełączają w trybie GATE i dają powtarzalny impuls w trybie TRIG. Masy rozdzielone (rozłącz połączenie mas z Kroku 3).

---

## Zadanie 5: Wiercenie obudowy

Wykonaj dla każdego pedału osobno. Zacznij od SMMH.

- [ ] **Krok 1: Zaplanuj rozmieszczenie otworów**

  Narysuj ołówkiem / na taśmie malarskiej:
  - 3× otwór na gniazda 3.5mm (PJ398SM — zwykle ~6 mm; zmierz suwmiarką gwint swoich gniazd)
  - 3× otwór na przełączniki toggle (gwint 6 mm — zwykle otwór ~6,5 mm; zmierz suwmiarką)

  Sprawdź, czy otwory nie kolidują z elementami w środku (zmierz od krawędzi obudowy do elementów na PCB).

- [ ] **Krok 2: Zabezpiecz PCB pedału przed opiłkami**

  Wyjmij PCB z obudowy (odkręć nakrętki potencjometrów i gniazd). Jeśli się nie da — szczelnie osłoń PCB folią i taśmą.

- [ ] **Krok 3: Wywierć otwory pilotażowe 2 mm**

- [ ] **Krok 4: Rozwierć do docelowej średnicy**

  Stopniowo: 2 mm → 4 mm → docelowa średnica. Usuń zadziory pilnikiem.

- [ ] **Krok 5: Usuń opiłki**

  Wydmuchaj i odkurz obudowę (i PCB, jeśli zostało w środku). Opiłek aluminium na PCB = zwarcie przy pierwszym włączeniu.

- [ ] **Krok 6: Przymierz gniazda i przełączniki**

  Wsuń bez przykręcania. Sprawdź, czy pasują i nie dotykają PCB pedału.

- [ ] **✓ Punkt przerwy 5:** Otwory wywiercone, opiłki usunięte, elementy pasują. To samo dla Cathedral.

---

## Zadanie 6: Instalacja w SMMH

- [ ] **Krok 1: Przylutuj krótkie przewody do padów tap SMMH**

  Na padach zaznaczonych w Zadaniu 1: krótki (~5 cm) czerwony przewód do tap_pin, krótki czarny do GND_ped. Minimum cyny, nie ruszaj sąsiednich elementów. Do tych krótkich przewodów dolutujesz w Krokach 5–6 REC i perfboard.

- [ ] **Krok 2: Zidentyfikuj wyprowadzenia gniazd PJ398SM (przed lutowaniem!)**

  PJ398SM ma 3 wyprowadzenia: tip, styk przełączany i sleeve. Włóż kabel patch do gniazda. Tryb ciągłości: końcówka (tip) wtyku ↔ wyprowadzenie, które piknie = **tip**; tuleja wtyku ↔ wyprowadzenie, które piknie = **sleeve**. Trzecie wyprowadzenie zostaw wolne. Oznacz markerem.

- [ ] **Krok 3: Zamontuj gniazda 3.5mm**

  Przykręć PJ398SM. Przylutuj:
  - tip jacka A → lewy terminal SELECT
  - tip jacka B → prawy terminal SELECT
  - tip jacka C → niebieski drut (in_C)
  - sleeve wszystkich trzech jacków → zielony drut (GND_mod)

- [ ] **Krok 4: Zamontuj SELECT (ON/OFF/ON) i ustal jego pozycje**

  Środkowy terminal (common) → żółty drut (in_AB). Lewy → jack A, prawy → jack B.
  Tryb ciągłości: środkowy terminal ↔ terminal jacka A, przełączaj dźwignię → pozycja, w której piknie = **A**. Analogicznie **B**. Pozycja środkowa = OFF. Opisz obudowę.

- [ ] **Krok 5: Zamontuj GATE/TRIG (ON/OFF) i ustal jego pozycje**

  Dwa białe druty (in_AB i node_h) do dwóch terminali przełącznika.
  Tryb ciągłości na dwóch terminalach, przełączaj dźwignię → pozycja, w której piknie = **GATE**; druga = **TRIG**. Opisz obudowę.

- [ ] **Krok 6: Zamontuj REC (ON/OFF) i podłącz perfboard**

  - REC: terminal 1 → krótki czerwony przewód (tap_pin SMMH), terminal 2 → krótki czarny przewód (GND_ped SMMH).
  - Czerwony drut z perfboardu (tap_pin) → krótki czerwony przewód tap_pin. Zaizoluj koszulką termokurczliwą.
  - Czarny drut z perfboardu (GND_ped) → krótki czarny przewód GND_ped. Zaizoluj koszulką.
  - Zielony (GND_mod) → sleeve jacków **TYLKO** — nigdy do GND pedału ani do obudowy.
  - Ustaw REC w pozycji OFF.

- [ ] **Krok 7: Przymocuj perfboard**

  Taśma dwustronna piankowa lub klej na gorąco. Perfboard nie może dotykać PCB pedału ani metalowej obudowy (podłóż kapton).

- [ ] **Krok 8: Kontrola izolacji w obudowie**

  Pedał odłączony od zasilania.

  - Najpierw sprawdź sondy: goły metal obudowy (śruba dna lub tuleja gniazda audio pedału) ↔ pad GND_ped → **piknięcie** ✓. Jeśli nie piknie — szukaj punktu z gołym metalem (lakier i anodowanie izolują).
  - GND_mod (sleeve dowolnego jacka CV) ↔ ten sam punkt obudowy → **brak piknięcia** ✓.
  - Tip każdego jacka CV ↔ ten sam punkt obudowy → **brak piknięcia** ✓.

  Jeśli piknie — coś ze strony modulara dotyka obudowy (najczęściej gniazdo lub drut przy otworze). Znajdź i odizoluj.

- [ ] **✓ Punkt przerwy 6:** SMMH złożony, wszystkie połączenia wykonane, izolacja potwierdzona.

---

## Zadanie 7: Testy funkcjonalne SMMH

Przed włączeniem zasilania: REC w pozycji OFF.

- [ ] **Krok 1: REC** — włącz REC na ~1 s → SMMH nagrywa pętlę (≥ 0,5 s przytrzymania). Wyłącz → pętla gra ✓.
- [ ] **Krok 2: Test ręczny wejścia C** — +5V przez rezystor 1kΩ na tip jacka C, minus na sleeve. Dotknij i puść kilka razy w równym tempie (~1 na sekundę) → SMMH ustawia czas delay ✓ (każde dotknięcie = jeden tap). **Nie** zwieraj tip ze sleeve — to nic nie da (strona modulara nie ma zasilania).
- [ ] **Krok 3: Wejścia A i B** — +5V przez rezystor 1kΩ na tip jacka A, minus na sleeve, SELECT na A, GATE/TRIG na TRIG. Dotknij i puść kilka razy w równym tempie → SMMH ustawia czas delay ✓. Powtórz dla jacka B z SELECT na B ✓.
- [ ] **Krok 4: Minimalny impuls (najważniejszy pomiar!)** — sekwencer z regulowaną długością gate → wejście A, GATE/TRIG na **GATE**. Zacznij od gate 50 ms i skracaj (50 → 20 → 10 → 5 → 2 → 1 ms). Przy każdej długości zmień tempo sekwencera (np. 120 → 80 BPM): tap jest łapany, gdy czas delay podąża za tempem. Zapisz najkrótszy gate, który SMMH jeszcze łapie. Jeśli oscyloskopem możesz zmierzyć długość gate — zmierz.
  - wynik ≤ 10 ms → OK, zostaje 0.22µF ✓
  - wynik > 10 ms → wymień C1 i C2 na **0.33µF** (zapas z zakupów) i powtórz Kroki 2, 3 i 5
  Wynik dopisz do spec.md, sekcja „Wymagania czasowe pedałów”.
- [ ] **Krok 5: Próg przytrzymania** — GATE/TRIG na **TRIG**, gate 3 s na wejście A → SMMH robi **jeden tap**, nie nagrywa pętli ✓. To samo na wejściu C ✓. Przełącz na **GATE** → gate 3 s nagrywa pętlę ✓ (zgodnie z zamierzeniem).
- [ ] **Krok 6: Tempo z sekwencera** — zegar 120 BPM (gate 50%) na wejście C → delay synchronizuje się z tempem ✓. Powtórz z gate 90% przy 300 BPM → każdy krok łapany ✓.
- [ ] **Krok 7: Brak humu** — SMMH do wzmacniacza, modular podłączony do jacka C, cisza na wejściu gitary → brak humu i brzęczenia ✓.

- [ ] **✓ Punkt przerwy 7:** SMMH działa, minimalny impuls zapisany. Zamknij obudowę.

---

## Zadanie 8: Instalacja i testy Cathedral

### Instalacja

- [ ] **Krok 1: Przylutuj krótkie przewody do padów tap Cathedral**

  Na padach zaznaczonych w Zadaniu 1: krótki (~5 cm) czerwony przewód do tap_pin, krótki czarny do GND_ped. Minimum cyny, nie ruszaj sąsiednich elementów.

- [ ] **Krok 2: Zidentyfikuj wyprowadzenia gniazd PJ398SM (przed lutowaniem!)**

  Włóż kabel patch do gniazda. Tryb ciągłości: końcówka (tip) wtyku ↔ wyprowadzenie, które piknie = **tip**; tuleja wtyku ↔ wyprowadzenie, które piknie = **sleeve**. Trzecie wyprowadzenie zostaw wolne. Oznacz markerem.

- [ ] **Krok 3: Zamontuj gniazda 3.5mm**

  Przykręć PJ398SM. Przylutuj: tip A → lewy terminal SELECT, tip B → prawy terminal SELECT, tip C → niebieski drut (in_C), sleeve wszystkich trzech → zielony drut (GND_mod).

- [ ] **Krok 4: Zamontuj SELECT (ON/OFF/ON) i ustal jego pozycje**

  Środkowy terminal (common) → żółty drut (in_AB). Lewy → jack A, prawy → jack B.
  Tryb ciągłości: środkowy terminal ↔ terminal jacka A, przełączaj dźwignię → pozycja, w której piknie = **A**. Analogicznie **B**. Pozycja środkowa = OFF. Opisz obudowę.

- [ ] **Krok 5: Zamontuj GATE/TRIG (ON/OFF) i ustal jego pozycje**

  Dwa białe druty (in_AB i node_h) do dwóch terminali. Tryb ciągłości na dwóch terminalach, przełączaj dźwignię → pozycja, w której piknie = **GATE**; druga = **TRIG**. Opisz obudowę.

- [ ] **Krok 6: Zamontuj REC (ON/OFF) i podłącz perfboard**

  - REC: terminal 1 → krótki czerwony przewód (tap_pin Cathedral), terminal 2 → krótki czarny przewód (GND_ped Cathedral).
  - Czerwony drut z perfboardu → krótki czerwony przewód tap_pin; czarny → krótki czarny GND_ped. Zaizoluj koszulką termokurczliwą.
  - Zielony (GND_mod) → sleeve jacków **TYLKO**.
  - Ustaw REC w pozycji OFF.

- [ ] **Krok 7: Przymocuj perfboard**

  Taśma dwustronna piankowa lub klej na gorąco, z kaptonem od strony PCB i obudowy.

- [ ] **Krok 8: Kontrola izolacji w obudowie**

  Pedał odłączony od zasilania.

  - Najpierw sprawdź sondy: goły metal obudowy (śruba dna lub tuleja gniazda audio pedału) ↔ pad GND_ped → **piknięcie** ✓.
  - GND_mod (sleeve dowolnego jacka CV) ↔ ten sam punkt obudowy → **brak piknięcia** ✓.
  - Tip każdego jacka CV ↔ ten sam punkt obudowy → **brak piknięcia** ✓.

  Jeśli piknie — znajdź i odizoluj.

### Testy

Przed włączeniem zasilania: REC w pozycji OFF.

- [ ] **Krok 9: REC** — włącz REC na ~1 s (> 350 ms) → **infinite reverb** (wybrzmienie się nie wycisza) ✓. Wyłącz → normalna praca ✓. (W trybie ECHO infinite nie działa — test w innym trybie.)
- [ ] **Krok 10: Test ręczny wejścia C** — +5V przez rezystor 1kΩ na tip jacka C, minus na sleeve. Dotknij i puść kilka razy w równym tempie (~1 na sekundę) → Cathedral ustawia pre-delay ✓ (każde dotknięcie = jeden tap). **Nie** zwieraj tip ze sleeve.
- [ ] **Krok 11: Wejścia A i B** — +5V przez rezystor 1kΩ na tip jacka A, minus na sleeve, SELECT na A, GATE/TRIG na TRIG. Dotknij i puść kilka razy w równym tempie → Cathedral ustawia pre-delay ✓. Powtórz dla jacka B z SELECT na B ✓.
- [ ] **Krok 12: Minimalny impuls** — sekwencer z regulowaną długością gate → wejście A, GATE/TRIG na **GATE**. Skracaj gate 50 → 20 → 10 → 5 → 2 → 1 ms. Przy każdej długości zmień tempo sekwencera (np. 120 → 80 BPM): tap jest łapany, gdy pre-delay podąża za tempem. Zapisz najkrótszy gate rozpoznawany jako tap.
  - wynik ≤ 10 ms → OK ✓
  - wynik > 10 ms → wymień C1 i C2 w Cathedral na **0.33µF** i powtórz Kroki 10, 11 i 13
  Wynik dopisz do spec.md, sekcja „Wymagania czasowe pedałów”.
- [ ] **Krok 13: Próg przytrzymania** — GATE/TRIG na **TRIG**, gate 3 s na wejście A → **jeden tap, bez infinite** ✓. To samo na wejściu C ✓. Przełącz na **GATE** → gate 3 s włącza infinite ✓.
- [ ] **Krok 14: Tempo z sekwencera** — zegar 120 BPM (gate 50%) na wejście C → pre-delay synchronizuje się ✓. Powtórz z gate 90% przy 300 BPM → każdy krok łapany ✓.
- [ ] **Krok 15: Brak humu** — Cathedral do wzmacniacza, modular podłączony do jacka C → brak humu ✓.

  **Uwaga:** podczas tapowania reverb krótko się urywa — to zachowanie firmware Cathedral, nie błąd moda.

- [ ] **✓ Punkt przerwy 8:** Cathedral działa, minimalny impuls zapisany. Zamknij obudowę.

---

## Troubleshooting

| Objaw | Możliwa przyczyna | Co zrobić |
|---|---|---|
| Nic nie działa, test diod przy PC817: 0.5–0.7V / OL | D1/D2 odwrotnie (ten sam kierunek co LED) | Wylutuj i odwróć diodę: pasek do pin 1 |
| GATE działa, TRIG nie | Impuls za krótki dla pedału | C1/C2 → 0.33µF |
| TRIG nie działa, GATE też nie | Złe nóżki Q1/Q2 albo D3/D4 odwrotnie | Sprawdź opis nóżek z Zadania 2; test D3/D4 z Zadania 3 Krok 6 |
| Pin 4 OC spada tylko do 1–4V zamiast ~0V | Zamienione C i E w Q1/Q2 | Wylutuj tranzystor, zidentyfikuj nóżki ponownie (Zadanie 2 Krok 4, gniazdo hFE) |
| Tylko pierwszy tap działa, kolejne nie | Brak R7/R8 lub zimny lut na R7/R8 | Sprawdź R7 (in_AB ↔ GND_mod) i R8 (in_C ↔ GND_mod): 100kΩ |
| Tap nie działa w ogóle | Zamienione tap_pin i GND_ped | Zmierz ponownie pady (Zadanie 1) |
| Wejście działa tylko bez wtyku albo wcale | Przylutowany styk przełączany gniazda zamiast tip | Zadanie 6 Krok 2 — identyfikacja wyprowadzeń |
| Pedał wchodzi w looper / infinite w trybie TRIG | GATE/TRIG opisany odwrotnie, zwarty albo C1 zwarty | Zadanie 6 Krok 5; sprawdź C1 |
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
