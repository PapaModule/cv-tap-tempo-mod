# CV Tap Tempo Mod — EHX SMMH + EHX Cathedral

**Data:** 2026-05-29  
**Aktualizacja:** 2026-06-04 — izolacja galwaniczna (BC547 → PC817)  
**Aktualizacja:** 2026-10-08 — v3: tranzystor w torze LED (filtr HP v2 dawał impuls ~0,1 ms), ujednolicona dioda antyparalel, przełącznik GATE/TRIG, poprawione testy  
**Status:** Do akceptacji

---

## Cel

Modyfikacja dwóch pedałów efektów:
- EHX Stereo Memory Man with Hazarai (SMMH)
- EHX Cathedral

Każdy pedał otrzymuje niezależny obwód dodający trzy wejścia CV trigger/gate z Eurorack, które sterują funkcją tap tempo. Projekt oparty na modyfikacji navs.modular.lab.

---

## Architektura

Dwa osobne, identyczne obwody — jeden na pedał. Każdy montowany na płytce perforowanej (perfboard) wewnątrz obudowy pedału.

### Zasada działania

Przycisk tap w obu pedałach działa identycznie: pin MCU trzymany wysoko (~3.3V), wciśnięcie przycisku zwiera go do GND. Obwód symuluje to zwarcie przez optoizolator PC817. GND modulara i GND pedału są galwanicznie odizolowane — brak ryzyka pętli masy.

Strona modulara nie ma własnego zasilania — cała energia pochodzi z sygnału CV:
- LED optoizolatora jest zasilana z CV przez rezystor 470Ω,
- tranzystor Q (BC547) w szeregu z LED działa jak „furtka”: przewodzi tylko wtedy, gdy filtr HP podaje prąd na bazę,
- filtr HP steruje bazą (wysoka impedancja), więc mały kondensator 0,22 µF wystarcza na impuls rzędu dziesiątek ms.

---

## Wymagania czasowe pedałów

Długość impulsu tap musi mieścić się między debounce MCU a progiem przytrzymania:

| Pedał | Przytrzymanie krótsze niż… | …jest tapem; dłuższe = | Źródło |
|---|---|---|---|
| SMMH | 0,5 s | nagrywanie / overdub pętli (w trybie MULTI TAP-1 SEC + REV: odtwarzanie wsteczne od chwili wciśnięcia) | manual EHX SMMH — zweryfikowane |
| Cathedral | 350 ms | infinite reverb (wszystkie tryby poza ECHO) | manual Cathedral wg wyników wyszukiwania — **niezweryfikowane**, przyjęte jako założenie |

- **Minimalna długość impulsu (debounce MCU): nieznana** — EHX jej nie publikuje. Do zmierzenia w teście „minimalny impuls” (plan.md).
- **Cel projektowy:** impuls w trybie TRIG rzędu kilkunastu–stu kilkudziesięciu ms (jak w oryginale navs, filtr HP ~1–3 Hz), z ponad dwukrotnym zapasem poniżej 350 ms przy najgorszym rozrzucie elementów.

---

## Wejścia i sterowanie

### Wejście A i B (przełączane)
- Dwa gniazda 3.5mm mono
- Przełącznik **SELECT** (3-pozycyjny ON/OFF/ON): wybiera aktywne wejście — A, wyłączone, lub B
- Przełącznik **GATE/TRIG** (2-pozycyjny ON/OFF, w schemacie SW_HP) dla aktywnego toru A/B:
  - **GATE** (ON, styk zwarty): tap trwa tyle, co gate — długi gate = przytrzymanie (SMMH: pętla, Cathedral: infinite)
  - **TRIG** (OFF, styk rozwarty): każdy gate skrócony do impulsu ~15–133 ms (zależnie od amplitudy CV, modułu i rozrzutu elementów); krótsze triggery przechodzą bez zmian
- Oba wejścia mogą mieć podłączone sygnały jednocześnie bez ryzyka — SELECT fizycznie rozłącza nieaktywną gałąź

### Wejście C
- Gniazdo 3.5mm mono
- Zawsze aktywne, nie podlega przełącznikowi SELECT
- Zawsze w trybie TRIG (filtr HP na stałe)

### Przełącznik REC
- 2-pozycyjny ON/OFF
- Bezpośrednie zwarcie tap_pin do GND_pedału — symuluje przytrzymanie przycisku
- **SMMH:** nagrywanie pętli / overdub (gdy włączony ≥0,5 s)
- **Cathedral:** infinite reverb (gdy włączony >350 ms)

---

## Schemat obwodu

Jeden tor (tor A/B; tor C identyczny, bez SELECT i bez SW_HP):

```
──────────────── STRONA MODULARA (GND_mod) ─────────────────┬── STRONA PEDAŁU (GND_ped) ──
                                                            │  (izolacja galwaniczna)
CV_A ──┐                                                    │
       ├──[SELECT A/OFF/B]── node_in                        │
CV_B ──┘                        │                           │
                                │                           │
  TOR LED:                      │                           │
     node_in ──[R2 470Ω]── LED+ ═ pin1 ┐                    │
                            │          │ OC1 PC817          │ pin4 (C) ──► tap_pin
                     D1 (antyparalel)  │ (LED)              │ pin3 (E) ──── GND_ped
                            │          │                    │
                           LED− ═ pin2 ┘                    │
                            │                               │
                       kolektor Q1 (BC547)                  │
                       emiter Q1 ── GND_mod                 │
                                                            │
  STEROWANIE BAZY (filtr HP):                               │
     node_in ──[C1 0.22µF]── node_h ──[R5 47kΩ]── baza Q1   │
     node_in ──[SW_HP GATE/TRIG]── node_h  (równolegle C1)  │
     node_h ──[R1 100kΩ]── GND_mod                          │
     node_in ──[R7 47kΩ]── GND_mod  (pull-down wejścia)     │
     baza Q1 ──[D3: katoda]  [D3: anoda]── GND_mod          │

REC switch ─────────────────────────────── tap_pin ──── GND_ped
```

**Definicje kierunków diod (obowiązują we wszystkich dokumentach i w schemacie):**
- **D1 / D2 — antyparalel do LED:** katoda D → pin1 PC817 (anoda LED), anoda D → pin2 PC817 (katoda LED). Przy normalnej pracy D jest zaporowo; przy ujemnym napięciu na LED przewodzi i ogranicza napięcie wsteczne LED do ~−0,7V. **Nigdy** w tym samym kierunku co LED — wtedy dioda (Vf ≈ 0,65V) przejmuje cały prąd i LED nie świeci.
- **D3 / D4 — klamp bazy:** anoda → GND_mod, katoda → baza Q. Ogranicza ujemne napięcie baza-emiter do ~−0,7V (BC547: max 6V wstecz) — przy opadającym zboczu gate'a i przy ujemnym CV.

**PC817 (DIP-4):** pin 1: LED(+), pin 2: LED(−), pin 3: E, pin 4: C  
**BC547 (TO-92):** pinout różni się między producentami — sprawdzić w datasheecie konkretnego egzemplarza przed lutowaniem.

### Połączenia toru (lista netów)

| Net | Elementy |
|---|---|
| node_in | SELECT common (tor A/B) lub tip jacka C (tor C), R2, C1, R7, SW_HP (tylko A/B) |
| LED+ | R2, pin1 OC1, katoda D1 |
| LED− | pin2 OC1, anoda D1, kolektor Q1 |
| node_h | C1, R1 (100k), R5 (47k), SW_HP (tylko A/B) |
| baza | R5, baza Q1, katoda D3 |
| GND_mod | emiter Q1, R1, R7, anoda D3, sleeve wszystkich jacków |
| tap_pin | pin4 OC1, pin4 OC2, REC |
| GND_ped | pin3 OC1, pin3 OC2, REC |

### Jak działa filtr HP (tryb TRIG)

- Narastające zbocze gate'a przechodzi przez C1 na węzeł node_h → prąd bazy przez R5 → Q1 przewodzi → LED świeci → fototranzystor zwiera tap_pin do GND_ped.
- C1 ładuje się przez R1 i R5; po ~15–133 ms (patrz „Parametry”) prąd bazy spada, Q1 przestaje przewodzić — tap się kończy, nawet jeśli gate trwa dalej.
- Na opadającym zboczu node_h idzie poniżej zera; D3 trzyma bazę na ~−0,7V, C1 rozładowuje się (τ ≈ 0,22 µF × 32 kΩ ≈ 7 ms) i obwód jest gotowy na następny gate.
- Gate krótszy niż czas impulsu (np. trigger 1–10 ms) przechodzi bez zmian — LED gaśnie razem z końcem gate'a, bo traci zasilanie.
- **R7 (pull-down 47kΩ)** ściąga wejście do 0V, gdy źródło przestaje wymuszać napięcie (odłączony przewód w teście ręcznym, wyjście modułu przez diodę, SELECT w pozycji OFF). Bez R7 C1 zostaje naładowany i kolejny gate nie daje tapu (symulacja: 1 z 3 dotknięć); z R7 C1 rozładowuje się ze stałą czasową τ ≈ 0,22 µF × (47 kΩ + ~32 kΩ) ≈ 17 ms (3 z 3 przy 1 s dotyku i 1 s przerwy). Wyjście modułu przez diodę przy gate 90% @ 300 BPM (przerwa 20 ms): najkrótszy impuls 17,8 ms przy 5V (ze 100 kΩ było 4,3 ms — dlatego 47 kΩ). Impulsy krótsze o ≤3,5% niż bez R7; wszystkie liczby w „Parametrach” policzone już z R7.

### Tryb GATE (SW_HP zwarty)

SW_HP zwiera C1: baza dostaje prąd przez R5 przez cały czas trwania gate'a, tap trwa tyle co gate.

---

## Parametry (z symulacji ngspice, `sim/run.sh`)

Założenia tabel nominalnych: tap aktywny, gdy prąd LED > 1 mA (PC817 nie jest modelowany — patrz „Weryfikacja”), hFE BC547 = 400, C nominalne. Wpływ tych założeń — w tabeli „Rozrzut” niżej. Rs = rezystancja wyjścia modułu (typowo ~1kΩ, część modułów bez rezystora = 0Ω).

**Długość impulsu w trybie TRIG (gate dłuższy niż impuls), wartości nominalne:**

| CV | Rs = 0Ω | Rs = 1kΩ |
|---|---|---|
| 5V | 19 ms | 34 ms |
| 10V | 25 ms | 74 ms |
| 12V | 26 ms | 86 ms |

**Rozrzut — najgorsze przypadki.** Rzeczywisty próg tapu jest nieznany: zależy od prądu pull-upu MCU i CTR egzemplarza PC817, więc może być znacznie niższy niż 1 mA (niższy próg = dłuższy impuls). Wzmocnienie BC547 zależy od grupy: A ≈ 110–220, B ≈ 200–450, C ≈ 420–800. Sprawdzone: próg 1 mA i 0,1 mA, tolerancja C ±10%; minimum przy 5V / Rs=0Ω / C−10%, maksimum przy 12V / Rs=1kΩ / C+10%.

| C1/C2 | BC547B (hFE 200–450) | dowolna grupa (hFE 110–800) |
|---|---|---|
| **0,22 µF (podstawowa)** | **15–133 ms** | 12–162 ms |
| 0,33 µF (zapasowa) | 22–199 ms | 19–243 ms |
| 0,47 µF (odrzucona) | 32–283 ms | 27–346 ms — praktycznie bez zapasu do 350 ms |

Wartości z `sim/run.sh` (z R7 = 47 kΩ), zaokrąglone na zewnątrz: minima w dół, maksima w górę. Wniosek: z 0,22 µF maksimum jest ≥2,6× poniżej 350 ms dla grupy B (≥2,1× dla dowolnej grupy). W BOM: **BC547B**.

Prostokąt bipolarny (skok z −V na +V, a nie od 0V) daje dłuższy impuls: najgorzej 168 ms przy ±12V, Rs = 1kΩ, hFE 800, C+10%, progu 0,1 mA — nadal ≥2× poniżej 350 ms.

**Prąd LED (szczyt):**

| CV | Rs = 0Ω | Rs = 1kΩ |
|---|---|---|
| 5V | 6,5 mA | 2,1 mA |
| 10V | 17 mA | 5,4 mA |
| 12V | 21 mA | 6,7 mA |

- Max prąd LED PC817 (abs. max): 50 mA — zapas wystarczający także przy 12V bez rezystora wyjściowego.
- CTR PC817: wg datasheetu min. 50% (nierangowany, do potwierdzenia w datasheecie dostawcy) — przy 2 mA LED fototranzystor może przewodzić ≥1 mA, wielokrotnie więcej niż prąd pull-upu MCU (ułamek mA). Potwierdza to test w plan.md.
- **R2 = 470Ω zostaje.** Zmniejszenie do 330/220Ω przy module 1kΩ zwiększa prąd LED tylko o 0,2–0,4 mA (ogranicza go rezystor w module), a przy module bez rezystora podnosi prąd do 30–45 mA (blisko limitu LED i wydajności op-ampów).

**Przypadki brzegowe (Rs = 1kΩ, 5V i 10V) — wszystkie tapy rejestrowane:**
- trigger 1 ms i 10 ms co 500 ms — przechodzą bez zmian (1 ms / 10 ms)
- gate 50% przy 120 BPM i gate 90% przy 300 BPM (przerwa 20 ms) — 10/10 impulsów, 31–75 ms
- gate 3 s w trybie TRIG — jeden impuls 34/74 ms; w trybie GATE — 3 s
- wyjście modułu przez diodę (nie ściąga do 0V), gate 90% @ 300 BPM — 10/10 impulsów, najkrótszy 17,8 ms (5V) / 58,9 ms (10V)

**Sygnały bipolarne do 20 Vpp (±10V) i 24 Vpp (±12V)** — LFO, oscylatory, wyjścia ±10V; sprawdzone: sinus ±10V 1 Hz i 1 kHz, prostokąt ±10V 1 kHz, prostokąt ±12V 2 Hz, stałe +12V; oba tryby; źródło 0Ω (najgorszy przypadek):

| Wielkość | Najgorszy przypadek | Limit | Zapas |
|---|---|---|---|
| Napięcie wsteczne baza-emiter Q1 | −0,70 V (klamp D3) | 6 V | 8× |
| Napięcie wsteczne LED PC817 | −0,73 V (klamp D1) | 6 V | 8× |
| Prąd LED | 21 mA | 50 mA | 2,4× |
| Moc na R2 (470Ω) | 211 mW ciągle (+12V, tryb GATE) | 600 mW (rezystor 0,6 W) | 2,8× |
| Prąd pobierany z modułu | ≤ 21 mA (ograniczony przez R2) | — | — |

- Przy ujemnym napięciu prąd płynie przez D1 i złącze baza-kolektor Q1 do D3 (ograniczony przez R2) — także w trybie TRIG, więc R2 grzeje się również przy ujemnych połówkach. Dlatego **R2/R4 = 0,6 W**: zwykły rezystor 1/4 W pracowałby na 85% mocy znamionowej.
- Obwód nie ulega uszkodzeniu przy żadnym sygnale z zakresu ±12V (pełny zakres zasilania Eurorack).

---

## Lista komponentów (na jeden pedał)

| Oznaczenie | Element | Wartość | Ilość |
|---|---|---|---|
| OC1, OC2 | Optoizolator | PC817, obudowa **DIP-4** (nie PC817S / wersje SMD) | 2 |
| Q1, Q2 | Tranzystor NPN | **BC547B**, TO-92 (A lub C też działają z 0,22 µF) | 2 |
| D1–D4 | Dioda małosygnałowa | 1N4148, obudowa **DO-35** (szklana, przewlekana; nie SOD-123 / MiniMELF) | 4 |
| R2, R4 | Rezystor (LED) | 470Ω, **0,6 W** metalizowany, przewlekany (rozmiar jak 1/4 W) | 2 |
| R5, R6 | Rezystor (baza) | 47kΩ, 1/4W, przewlekany | 2 |
| R1, R3 | Rezystor (shunt HP) | 100kΩ, 1/4W, przewlekany | 2 |
| R7, R8 | Rezystor (pull-down wejścia) | 47kΩ, 1/4W, przewlekany | 2 |
| C1, C2 | Kondensator filmowy | 0.22µF, 63V+, radialny, raster 5 mm | 2 |
| SELECT | Przełącznik 3-poz. ON/OFF/ON | SPDT mini toggle | 1 |
| GATE/TRIG, REC | Przełącznik 2-poz. ON/OFF | SPST mini toggle | 2 |
| — | Gniazdo 3.5mm mono, **izolowane od panelu** | Thonkiconn PJ398SM lub ekw. | 3 |
| — | Płytka perforowana | rozmiar ustalony w plan.md po rozplanowaniu layoutu | 1 |

**Wszystkie elementy są przewlekane (THT) — brak SMD.** Przy zakupie pilnować oznaczeń obudów z tabeli.

**Łącznie na oba pedały:** ×2 każdego elementu. Zapas: 2× kondensator 0,33 µF na wypadek wymiany (patrz „Weryfikacja”).

Tor C: C2, R3, R6, R4, R8, D2, D4, Q2, OC2 — numeracja analogiczna do toru A/B (R8 w torze C odpowiada R7).

**Uwaga:** kondensatory C1/C2 filmowe (niepolarne) — na node_h pojawia się napięcie ujemne przy opadającym zboczu.

---

## Montaż

1. Wywiercić otwory w obudowie pedału na 3 gniazda 3.5mm i 3 przełączniki
2. Zmontować obwód na perfboardzie (dwie oddzielne szyny GND_mod i GND_ped)
3. Zlokalizować na PCB pedału punkty lutownicze przycisku tap (dwa pady: tap_pin i GND_ped)
4. Podłączyć pin 4 (C) PC817 do tap_pin, pin 3 (E) do GND_pedału
5. Emiter Q, R1/R3, R7/R8, D3/D4 i sleeve jacków do GND_modulara — **nigdy** do GND pedału
6. Przełącznik REC bezpośrednio między tap_pin a GND_pedału
7. **Kontrola izolacji:** multimetr (ciągłość) między GND_mod a metalową obudową pedału → brak przejścia. Sleeve jacków i elementy strony modulara nie mogą dotykać obudowy (obudowa = GND pedału).

---

## Weryfikacja

- **Tap pedałów:** tap_pin siedzi na ~3.3V, wciśnięcie zwiera do GND — do potwierdzenia pomiarem w obu pedałach (plan.md, Zadanie 1) przed montażem.
- **Izolacja:** PC817 zapewnia izolację galwaniczną — pod warunkiem kontroli z punktu 7 montażu.
- **Symulacja:** wszystkie liczby z sekcji „Parametry” odtwarzane przez `sim/run.sh` (ngspice). Ograniczenia modelu: LED PC817 modelowana behawioralnie (Vf ~1,2V @ 10 mA), fototranzystor niemodelowany — próg tapu przyjęty jako I_LED > 1 mA, a wpływ niższego progu (0,1 mA) i rozrzutu hFE sprawdzony w tabeli „Rozrzut”.
- **Testy funkcjonalne wymagane w plan.md:**
  - minimalny impuls: w trybie GATE najkrótszy gate rozpoznawany jako tap — wynik dopisać do sekcji „Wymagania czasowe”; jeśli przekracza 10 ms → wymienić C1/C2 na 0,33 µF (impuls 22–199 ms); 0,47 µF nie stosować (praktycznie bez zapasu do 350 ms)
  - próg przytrzymania: w trybie TRIG gate 3 s nie może włączyć pętli (SMMH) ani infinite (Cathedral)
  - test ręczny wejść: podanie 5V (np. zasilacz USB lub bateria 9V przez rezystor 1kΩ) na tip jacka — **nie** zwarcie tip–sleeve (strona modulara nie ma własnego zasilania)

---

## Znane ograniczenia

- **Cathedral:** podczas tapowania reverb krótko się urywa — ograniczenie firmware Cathedral, nie obwodu
- **REC:** w SMMH wchodzi w nagrywanie pętli, w Cathedral włącza infinite reverb — celowe, ale wymaga świadomości przy graniu
- **Tryb GATE:** gate dłuższy niż 350 ms (Cathedral) / 0,5 s (SMMH) zadziała jak przytrzymanie — celowe
- **Wolne LFO (sinus) w trybie TRIG:** łagodne zbocze daje słaby impuls (symulacja: prąd LED ~1,8 mA przy ±10V 1 Hz) — tap może być niepewny. Do sterowania z LFO używać trybu GATE albo sygnału prostokątnego.
- **Obciążenie modułu:** do 21 mA przy ±12V z wyjścia bez rezystora — bezpieczne dla typowych wyjść Eurorack, ale moduł z bardzo słabym wyjściem może obniżyć napięcie.
- **Długość impulsu TRIG zależy od amplitudy CV, wyjścia modułu i rozrzutu elementów** (15–133 ms z BC547B) — mieści się w wymaganiach dla wszystkich typowych źródeł

---

## Dlaczego v3 (błędy w v2)

1. **Filtr HP v2 dawał impuls ~0,1 ms, nie ~1 ms.** Obliczenie τ = 10k × 0,1µF = 1 ms pomijało obciążenie gałęzią 470Ω + LED (efektywnie ~450Ω → τ ≈ 45 µs). Symulacja: prąd LED > 1 mA przez 85–230 µs. Taki impuls najpewniej nie przejdzie przez debounce MCU — wejście C (zawsze z filtrem) mogło w ogóle nie działać. Ten sam błąd miała wersja z BC547 (przed 2026-06-04): baza sterowana przez 1kΩ, τ liczone bez obciążenia. v3 stosuje wysoką impedancję bazy, jak x37v (100k/10k) i navs (HP ~1–3 Hz).
2. **Trzy różne wersje diody D1/D2:** spec/README — antyparalel (poprawnie); schematic.svg — równolegle w tym samym kierunku co LED (symulacja: prąd LED ≈ 2 pA, mod nie działa); plan.md — szeregowo. Ujednolicone na antyparalel.
3. **Wariant odrzucony — sam większy kondensator (22 µF, układ v2):** impuls 21–50 ms, ale przy 5V i gate 90% @ 300 BPM rejestruje 1 z 10 tapów (kondensator nie zdąży się rozładować w 20 ms przerwy).
4. **Test ręczny „zwarcie tip do sleeve”** nie mógł zadziałać — strona modulara nie ma zasilania.
5. **Napis „HP ON”** oznaczał w rzeczywistości filtr wyłączony — zastąpiony GATE/TRIG.

---

## Źródła

- [EHX Stereo Memory Man with Hazarai — manual (PDF)](https://www.ehx.com/wp-content/uploads/2021/01/stereo-memory-man-with-hazarai-manual.pdf) — próg 0,5 s tap vs. pętla
- [EHX Cathedral — manual (ManualsLib)](https://www.manualslib.com/manual/2900221/Electro-Harmonix-Cathedral-Stereo-Reverb.html) — próg 350 ms (niezweryfikowany bezpośrednio)
- [navs.modular.lab — More Hazarai!](http://navsmodularlab.blogspot.com/2009/08/more-hazarai-ehx-smmh-modification.html) — filtr HP ~1–3 Hz, wejście C zawsze filtrowane
- [navs.modular.lab — Even More Hazarai!](http://navsmodularlab.blogspot.com/2011/10/even-more-hazarai.html)
- [GitHub: x37v/ehx-hazarai (KiCad)](https://github.com/x37v/ehx-hazarai) — HP 10nF/100k sterujący bazą BC547 przez 10k
- [How to Add Voltage Control to an EHX Cathedral](https://donotfuckup.home.blog/2019/03/09/how-to-add-voltage-control-to-an-ehx-cathedral/)
- [EHX Cathedral CV mod — MOD WIGGLER](https://modwiggler.com/forum/viewtopic.php?t=60110)
