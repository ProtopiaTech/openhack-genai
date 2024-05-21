# Zadanie 1: Ładowanie danych i ich klasyfikacja

TODO: @kaluzaaa python, @mgrabarz logicapps

## Opis

Twoim zadaniem jest przygotowanie procesu ładowania danych do Azure AI Search oraz wykonanie klasyfikacji załadowanych dokumentów. Dokumenty te mogą być klasyfikowane jako "Dane osobowe", "Prywatny" lub "Publiczny". Klasyfikacja musi być zapisana w polu typu "filterable", aby umożliwić użycie filtrów bezpieczeństwa (Security Filters) w Azure AI Search. Przykładowe pliki PDF znajdują się w katalogu `../data`.

Podczas klasyfikacji użyj angielskich nazw w formacie przyjaznym dla programowania: `personal_data` dla "Dane osobowe", `private` dla "Prywatny", oraz `public` dla "Publiczny". W kolejnym zadaniu zespół skorzysta z Security Filters, aby ograniczyć dostęp do dokumentów na podstawie ich klasyfikacji.

## Cele zadania

1. **Konfiguracja indeksu**:
   - Stworzenie i skonfigurowanie indeksu w Azure AI Search, który będzie zawierał odpowiednie pola do przechowywania informacji o dokumentach oraz ich klasyfikacji.
   - Dodanie pola typu "filterable" do indeksu, które będzie przechowywało informacje o klasyfikacji dokumentu.

2. **Załadowanie dokumentów i klasyfikacja**:
   - Przygotowanie procesu ładowania plików PDF do Azure AI Search.
   - Klasyfikacja każdego dokumentu na podstawie jego treści jako "Dane osobowe", "Prywatny" lub "Publiczny".
   - Zapisanie klasyfikacji w polu typu "filterable" podczas ładowania dokumentów do Azure AI Search.
   - W ten sposób załadujesz dane oraz dokonasz ich klasyfikacji w jednym kroku, co uprości cały proces i zapewni spójność danych.


## Jak można to zaimplementować?

## Przydatne informacje
