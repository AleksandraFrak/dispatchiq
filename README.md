# DispatchIQ

DispatchIQ to dynamiczna strona internetowa prezentująca koncepcję platformy wspierającej zarządzanie ratownictwem w czasie rzeczywistym. Projekt zawiera frontend, prosty backend HTTP oraz bazę danych SQLite.

## Cel projektu

Celem projektu jest zaprojektowanie oraz wykonanie responsywnej strony typu one-page, zgodnej z wymaganiami projektu zaliczeniowego. Strona prezentuje fikcyjny system DispatchIQ, który wspiera dyspozytornie, stacje pogotowia oraz inne służby w monitorowaniu zespołów, triażowaniu zgłoszeń i analizie danych.

## Technologie

- HTML5
- CSS3
- JavaScript
- Python 3
- SQLite
- Figma

## Funkcjonalności

- responsywna strona one-page
- menu nawigacyjne z przewijaniem do sekcji
- menu mobilne typu hamburger
- sekcja w układzie trzech kolumn
- backend zwracający dane w formacie JSON
- baza danych SQLite z przykładowymi zgłoszeniami
- dynamiczne pobieranie danych przez `fetch()`
- wyświetlanie zgłoszeń z bazy danych na stronie
- dodawanie, edycja i usuwanie zgłoszeń z poziomu strony
- komponent przycisku z wariantami w Figmie
- wykorzystanie zmiennych CSS
- semantyczna struktura HTML
- podstawowe elementy dostępności

## Struktura projektu

```text
dispatchiq/
├── index.html
├── style.css
├── script.js
├── backend/
│   ├── server.py
│   └── dispatchiq.db
├── README.md
├── analiza-ux.md
```

## Struktura projektu

- index.html — struktura strony, sekcje, nawigacja i treść.
- style.css — style, kolory, layout, responsywność i zmienne CSS.
- script.js — obsługa mobilnego menu hamburger, pobieranie zgłoszeń z API oraz formularz CRUD.
- backend/server.py — serwer HTTP, endpointy API, operacje CRUD i inicjalizacja bazy SQLite.
- backend/dispatchiq.db — baza danych tworzona automatycznie przy pierwszym uruchomieniu backendu.
- README.md
- analiza-ux.md

## Backend i API

Backend jest napisany w Pythonie i korzysta wyłącznie z bibliotek standardowych. Po uruchomieniu tworzy bazę SQLite oraz uzupełnia ją minimum 10 rekordami.

Dostępne endpointy:

```text
GET /api/incidents
POST /api/incidents
PUT /api/incidents/{id}
DELETE /api/incidents/{id}
```

Endpointy pobierają, dodają, edytują i usuwają zgłoszenia w bazie danych. Dane są zwracane w formacie JSON.

## Uruchomienie projektu

1. Pobierz repozytorium.
2. Otwórz folder projektu.
3. Uruchom backend:

```bash
python3 backend/server.py
```

4. Otwórz stronę w przeglądarce:

```text
http://127.0.0.1:8000
```

5. Endpoint API jest dostępny pod adresem:

```text
http://127.0.0.1:8000/api/incidents
```

Po uruchomieniu strony można zarządzać zgłoszeniami bezpośrednio w sekcji „Aktualne zgłoszenia z dyspozytorni”. Formularz dodaje nowe rekordy do bazy, a przyciski na kartach umożliwiają edycję i usuwanie istniejących zgłoszeń.

## Projekt w Figmie

https://www.figma.com/design/IZX5JwrvM0ii2TCEmG9jxS/DispatchIQ?node-id=0-1&t=Es6Nucltuk1ltzmq-1

## Autor 

**Aleksandra Frąk**

Informatyka II stopień, rok I, semestr II

Katolicki Uniwersytet Lubelski Jana Pawła II w Lublinie
