# Plant Watering Project

## Opis projektu

Plant Watering Project to aplikacja klient-serwer w Pythonie do monitorowania
i podlewania roślin domowych. Serwer przechowuje przykładowe obiekty roślin,
czujników wilgotności oraz harmonogramów podlewania. Klient łączy się z
serwerem TCP, podaje swoje ID i pobiera listy obiektów wybranych klas.

Projekt spełnia wymagania:

- minimum 3 klasy danych,
- serwer wielowątkowy,
- limit aktywnych klientów,
- serializacja obiektów przez `pickle`,
- obsługa błędnego typu danych po stronie klienta,
- testy jednostkowe i integracyjne,
- dokumentacja README.

## Skład zespołu

Adrian Pierzchała - całość projektu.

## Struktura projektu

```text
plant_watering_project/
├── models.py
├── storage.py
├── server.py
├── client.py
├── README.md
├── requirements.txt
└── tests/
    ├── test_models.py
    ├── test_storage.py
    ├── test_serialization.py
    └── test_client_server.py
```

## Instrukcja uruchamiania

Instalacja zależności:

```bash
pip install -r requirements.txt
```

Uruchomienie serwera:

```bash
python server.py
```

Uruchomienie klienta:

```bash
python client.py 1
```

Uruchomienie kilku klientów:

```bash
python client.py 1
python client.py 2
python client.py 3
python client.py 4
```

Serwer przyjmuje maksymalnie 3 aktywnych klientów. Czwarty klient otrzymuje
odpowiedź `REFUSED`.

## Uruchomienie testów

```bash
pytest
```

## Opis klas

### Plant

Klasa opisująca roślinę domową.

Pola:

- `name` - nazwa rośliny,
- `species` - gatunek,
- `water_need` - zapotrzebowanie na wodę.

### Sensor

Klasa opisująca czujnik wilgotności przypisany do rośliny.

Pola:

- `sensor_id` - identyfikator czujnika,
- `plant_name` - nazwa rośliny,
- `humidity` - odczyt wilgotności.

### WateringSchedule

Klasa opisująca harmonogram podlewania.

Pola:

- `plant_name` - nazwa rośliny,
- `hour` - godzina podlewania,
- `water_amount_ml` - ilość wody w mililitrach.

Każda klasa posiada konstruktor, metodę `__str__` oraz metodę `__eq__`.

## Storage

Plik `storage.py` zawiera funkcję `create_initial_data()`, która tworzy
po 4 obiekty klas `Plant`, `Sensor` i `WateringSchedule`. Obiekty są zapisane
w słowniku pod kluczami:

- `plant_1`, `plant_2`, `plant_3`, `plant_4`,
- `sensor_1`, `sensor_2`, `sensor_3`, `sensor_4`,
- `schedule_1`, `schedule_2`, `schedule_3`, `schedule_4`.

Funkcja `get_objects_by_class(data, class_name)` zwraca listę obiektów danej
klasy na podstawie jej nazwy.

## Opis protokołu komunikacji

Komunikacja odbywa się przez TCP:

- host: `localhost`,
- port: `5000`,
- limit klientów: `MAX_CLIENTS = 3`.

Przebieg komunikacji:

1. Klient łączy się z serwerem.
2. Klient wysyła swoje ID.
3. Serwer odpowiada `OK` albo `REFUSED`.
4. Po odpowiedzi `OK` klient wysyła kolejno zapytania:
   - `Plant`,
   - `Sensor`,
   - `WateringSchedule`,
   - `Animal`.
5. Serwer dla poprawnych klas odsyła listę obiektów zserializowaną przez
   `pickle`.
6. Przed danymi pickle serwer wysyła 4 bajty z rozmiarem wiadomości.
7. Dla nieistniejącej klasy, np. `Animal`, serwer celowo odsyła obiekt
   niepoprawnego typu.
8. Klient sprawdza typ odebranych danych i wypisuje błąd
   rzutowania/niepoprawnego typu danych.

Serwer obsługuje każdego klienta w osobnym wątku i dodaje losowe opóźnienia
`time.sleep(random.uniform(0.5, 2.0))`.

## Deklaracja użycia AI

W projekcie wykorzystano narzędzia AI, w tym ChatGPT/Codex, do przygotowania
szkieletu projektu, wygenerowania przykładowego kodu serwera i klienta,
przygotowania testów oraz pomocy w stworzeniu dokumentacji README. Kod został
przeanalizowany i dostosowany do wymagań projektu przez autora.
Przykladowe prompty: 
1. Przygotuj mi plan aplikacji do podlewania roslin w python, ktora spelnia wymagania z zalacznika.
2. Czy to repozytorium https://github.com/adekObiadek/PZIV2026L169108AP.git jest dobrym rozwiazaniem do wymagan z zalacznika.