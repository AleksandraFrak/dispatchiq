## Analiza UX

### Problem użytkownika

Ratownictwo medyczne i służby ratunkowe działają w środowisku, w którym bardzo ważny jest czas reakcji, szybki dostęp do informacji oraz sprawna koordynacja zespołów. Dyspozytorzy muszą analizować zgłoszenia, kontrolować dostępność jednostek i podejmować decyzje pod presją czasu. Brak czytelnego systemu może prowadzić do opóźnień, błędów komunikacyjnych oraz trudności w zarządzaniu zespołami.

Strona DispatchIQ odpowiada na potrzebę zaprezentowania rozwiązania, które wspiera organizację pracy dyspozytorni oraz pomaga w monitorowaniu działań ratowniczych w czasie rzeczywistym.

### Grupa docelowa

Główną grupą docelową są osoby i instytucje związane z ratownictwem oraz zarządzaniem sytuacjami kryzysowymi, w szczególności:

- dyspozytornie medyczne,
- stacje pogotowia,
- szpitale i SOR,
- straż pożarna,
- osoby decyzyjne odpowiedzialne za wdrażanie systemów informatycznych w ochronie zdrowia i służbach ratunkowych.

### Uzasadnienie struktury strony

Strona została zaprojektowana jako one-page, ponieważ jej celem jest szybkie przedstawienie najważniejszych informacji o produkcie. Użytkownik nie musi przechodzić między wieloma podstronami — wszystkie treści są dostępne w logicznej kolejności na jednej stronie.

Na początku znajduje się sekcja hero, która jasno komunikuje, czym jest DispatchIQ i do czego służy. Następnie użytkownik poznaje opis systemu, najważniejsze funkcje, dynamiczną listę zgłoszeń oraz grupy odbiorców. Na końcu znajduje się sekcja kontaktowa z przyciskiem CTA, dzięki czemu użytkownik może łatwo wykonać kolejną akcję.

Sekcja „Kluczowe informacje” została zaprojektowana w układzie trzech kolumn, aby czytelnie przedstawić trzy główne funkcje systemu: monitorowanie zespołów, triażowanie zgłoszeń oraz analitykę danych.

Sekcja „Aktualne zgłoszenia z dyspozytorni” pełni funkcję demonstracji działania systemu. Dane nie są wpisane na stałe w HTML, tylko pobierane dynamicznie z backendu i bazy SQLite. Dzięki temu użytkownik widzi, że strona nie jest jedynie prezentacją marketingową, ale posiada działającą warstwę aplikacyjną.

### Uzasadnienie funkcji dynamicznych

W projekcie dodano panel zgłoszeń, który pozwala pobierać, dodawać, edytować i usuwać rekordy. Jest to zgodne z kontekstem produktu, ponieważ dyspozytor pracuje właśnie na bieżących zgłoszeniach i musi mieć szybki dostęp do najważniejszych informacji.

Każde zgłoszenie jest prezentowane w formie karty. Taki układ pozwala szybko odczytać:

- kod zgłoszenia,
- priorytet,
- opis zdarzenia,
- dzielnicę,
- przypisaną jednostkę,
- status,
- szacowany czas dojazdu.

Priorytety są wyróżnione kolorystycznie, ponieważ w systemach ratowniczych informacja o pilności musi być widoczna natychmiast. Czerwony oznacza przypadki krytyczne, pomarańczowy wysoki priorytet, niebieski średni, a zielony niski. Taki podział pomaga użytkownikowi szybciej skanować listę i podejmować decyzje.

Formularz dodawania i edycji zgłoszeń znajduje się bezpośrednio nad listą danych. Dzięki temu użytkownik może wykonać podstawowe operacje bez przechodzenia do osobnej podstrony. Przyciski „Edytuj” i „Usuń” są umieszczone przy konkretnych kartach, co zmniejsza ryzyko pomylenia rekordów.

### Uzasadnienie kolorystyki i układu

W projekcie zastosowano ciemny granat jako kolor główny, ponieważ kojarzy się z profesjonalizmem, technologią, bezpieczeństwem i zaufaniem. Kolor czerwony pełni funkcję akcentu i został użyty głównie w przyciskach CTA, ponieważ przyciąga uwagę i nawiązuje do tematyki ratownictwa.

Jasne tła w sekcjach informacyjnych poprawiają czytelność treści i oddzielają poszczególne części strony. Karty oraz ikony pomagają szybciej zrozumieć funkcje systemu i ułatwiają skanowanie treści.

Układ strony został zaprojektowany tak, aby był prosty, przejrzysty i responsywny. Na większych ekranach dane są prezentowane w kolumnach, co ułatwia porównywanie zgłoszeń. Na mniejszych ekranach elementy przechodzą w jedną kolumnę, dzięki czemu formularz i karty pozostają czytelne na telefonach.

### Dostępność i czytelność

Projekt wykorzystuje semantyczne sekcje HTML, nagłówki, etykiety formularzy oraz widoczne stany fokusu dla linków, przycisków i pól formularza. Menu mobilne posiada atrybut `aria-expanded`, dzięki czemu jego stan może być odczytany przez technologie wspomagające.

Komunikaty formularza informują użytkownika, czy rekord został dodany, zaktualizowany lub usunięty. W przypadku braku połączenia z backendem strona wyświetla czytelną informację o problemie zamiast pustej sekcji.
