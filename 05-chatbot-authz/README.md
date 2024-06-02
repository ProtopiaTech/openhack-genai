## Zadanie 5: Rozszerzenie aplikacji o obsługę Security Filters

### Opis
Twoim zadaniem jest rozszerzenie aplikacji o obsługę Security Filters, które będą działać na podstawie ról użytkownika wynikających z grup przypisanych do niego w Entra ID (Azure AD). Role te są przechowywane w tokenie użytkownika jako lista w polu "roles".

Należy założyć odpowiednie grupy w Entra ID (Azure AD), które będą odpowiadały za role w aplikacji.

Endpoint aplikacji należy zmodyfikować, aby wymagał odpowiednich ról użytkownika do uzyskania dostępu, zgodnie z określonymi w mapowaniu ról. Lista ról będzie dostępna w funkcji obsługi endpointu, umożliwiając dalsze wykorzystanie informacji o rolach użytkownika wewnątrz funkcji.

Twoim zadaniem jest również napisanie kodu do dynamicznego generowania filtra do Azure Search na polu `data_classification`, korzystając z dostępnych ról.

Aby zaimplementować Security Filters, należy wymusić filtry na retriever. W tym celu trzeba zmodyfikować retriever, aby dodać pole `filters` w słowniku `search_kwargs`.

### Cele zadania

1. **Konfiguracja Entra ID (Azure AD)**:
   - Założenie odpowiednich grup w Entra ID (Azure AD) zgodnych z wartościami w mapowaniu ról.

2. **Modyfikacja endpointu**:
   - Zmiana dekoratora endpointu, aby wymagał odpowiednich ról użytkownika do uzyskania dostępu.

3. **Generowanie filtra**:
   - Napisanie kodu do dynamicznego generowania filtra do Azure Search na polu `data_classification`, korzystając z dostępnych ról użytkownika.

4. **Implementacja Security Filters**:
   - Modyfikacja retriever, aby dodać pole `filters` w słowniku `search_kwargs` i wymusić filtry na retriever.

5. **Testowanie i weryfikacja**:
   - Przeprowadzenie testów w celu zapewnienia poprawnego działania Security Filters.
   - Weryfikacja, czy użytkownicy z odpowiednimi rolami mają dostęp tylko do dozwolonych danych, zgodnie z klasyfikacją dokumentów.

### Jak zaimplementować?

1. **Konfiguracja Entra ID (Azure AD)**:
   - Załóż odpowiednie grupy w Entra ID (Azure AD), które będą odpowiadały za role w aplikacji. Upewnij się, że nazwy grup są zgodne z wartościami w `ROLES_MAPPING`.

2. **Modyfikacja endpointu**:
   - Zmodyfikuj endpoint `/chat`, aby wymagał odpowiednich ról użytkownika do uzyskania dostępu. Dekorator `requires_jwt_authorization` pozwala na przekazanie `roles`, czyli ID grup, które mają dostęp, oraz `roles_mapping`, czyli słownika, który mapuje ID grup na nazwy:
   ```python
   @app.route('/chat', methods=['POST'])
   @requires_jwt_authorization(roles=[PERSONAL_DATA_GROUP_ID], roles_mapping=ROLES_MAPPING)
   def chat(roles):
   ```
   - Dzięki temu endpoint będzie wymagał odpowiednich ról użytkownika do uzyskania dostępu, a lista ról (`roles`) będzie dostępna w funkcji do dalszego wykorzystania.

3. **Generowanie filtra**:
   - Napisz kod do dynamicznego generowania filtra do Azure Search na polu `data_classification`, korzystając z dostępnych ról użytkownika.
   - Przykładowy `filter_query`:
   ```python
   filter_query = "data_classification eq 'public' or data_classification eq 'private' or data_classification eq 'personal-data'"
   ```

4. **Implementacja Security Filters**:
   - Zmodyfikuj retriever o `search_kwargs`, aby dodać pole `filters` w słowniku `search_kwargs`:
   ```python
   retriever = vector_store.as_retriever(
       search_type="hybrid",
       search_kwargs={
           "filters": filter_query
       }
   )
   ```

5. **Testowanie i weryfikacja**:
   - Przeprowadź testy w celu zapewnienia poprawnego działania Security Filters.
   - Upewnij się, że użytkownicy z odpowiednimi rolami mają dostęp tylko do dozwolonych danych, zgodnie z klasyfikacją dokumentów.

### Przykład obiektu ROLES_MAPPING

```python
ROLES_MAPPING = {
    PUBLIC_GROUP_ID: "public",
    PRIVATE_GROUP_ID: "private",
    PERSONAL_DATA_GROUP_ID: "personal-data"
}
```

PUBLIC_GROUP_ID, PRIVATE_GROUP_ID, PERSONAL_DATA_GROUP_ID to zmienne, w których są przechowywane ID grup.

### Zmienne środowiskowe
Do zmiennych środowiskowych należy przekazać dwa parametry:
```bash
AUTHORITY=https://login.microsoftonline.com/cc58971a-0481-4ec0-bf8d-bb2e265db003 
ISSUER=https://sts.windows.net/cc58971a-0481-4ec0-bf8d-bb2e265db003/
```
Gdzie `cc58971a-0481-4ec0-bf8d-bb2e265db003` to Twój tenant ID.