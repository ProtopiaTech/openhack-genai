## Zadanie 4: Dodanie uwierzytelnienia do aplikacji chatbota z wykorzystaniem Entra ID (Azure AD)

### Opis
To zadanie jest kontynuacją rozszerzania aplikacji chatbot. Twoim zadaniem jest skonfigurowanie aplikacji do uwierzytelniania użytkowników za pomocą Entra ID (Azure AD). Bazowy kod aplikacji znajduje się w katalogu `src`. Aplikacja wymaga konfiguracji do realizacji authorization code flow with PKCE (Proof Key for Code Exchange).

### Cele zadania

1. Konfiguracja aplikacji w Entra ID (Azure AD).
2. Dodanie Redirect URIs.
3. Dodanie Application ID URI i skopu.
4. Dodanie group claim.
5. Dodanie uprawnień API.

### Jak zaimplementować?

#### Krok 1: Konfiguracja aplikacji w Entra ID (Azure AD)

1. **Zaloguj się do Azure Portal** i przejdź do sekcji Azure Active Directory.
2. **Zarejestruj nową aplikację**:
   - Nazwa: `TwojaNazwaAplikacji`
   - Typ konta: Konta w katalogu organizacji
   - URI przekierowania: Dodaj URI przekierowania, np. `http://localhost:5001`, `https://*.app.github.dev`, `https://<hostname Twojego appservice>`
3. **Zapisz Application ID nowo utworzonej aplikacji** i przekaż je jako zmienną do App Service o nazwie `CLIENT_ID`.
4. **Zapisz ID Tenant (Tenant ID) Entra ID** i przekaż je jako zmienną do App Service o nazwie `TENANT_ID`.

#### Krok 2: Dodanie Redirect URIs

1. W sekcji `Uwierzytelnianie` aplikacji Entra ID (Azure AD) dodaj następujące adresy URL jako Redirect URIs w sekcji "Add a platform" -> Single-page application:
   - `http://localhost:5001`
   - `https://*.app.github.dev`
   - `https://<hostname Twojego appservice>`

#### Krok 3: Dodanie Application ID URI i skopu

1. W sekcji `Expose an API` dodaj Application ID URI.
2. Dodaj nowy scope:
   - Nazwa: `chat`
   - `Who can consent?`: `Admins and users`

#### Krok 4: Dodanie group claim

1. W sekcji `Token configuration` dodaj group claim i zaznacz `Security groups`. Na każdej grupie zaznacz opcję `Emit groups as role claims`.

#### Krok 5: Dodanie uprawnień API

1. W sekcji `API permissions` dodaj uprawnienie `User.ReadBasic.All` z Microsoft Graph.

### Jak działa uwierzytelnianie w kodzie aplikacji

#### Frontend (`chatbot.js`)

1. **Konfiguracja MSAL.js**:
    - Na początku kodu zdefiniowane jest `msalConfig`, które zawiera `clientId` (identyfikator aplikacji), `authority` (adres URL Tenant) oraz `redirectUri` (adres, na który użytkownik zostanie przekierowany po uwierzytelnieniu).
    - `msalInstance` jest instancją `msal.PublicClientApplication`, która jest używana do interakcji z Entra ID (Azure AD).

2. **Żądanie logowania**:
    - `loginRequest` definiuje zakresy, które aplikacja będzie żądać, w tym `user.read` oraz `api://clientId/chat`, które są potrzebne do uzyskania dostępu do API.

3. **Inicjalizacja MSAL**:
    - Funkcja `initializeMsal` jest wywoływana, aby zainicjować MSAL.
    - `msalInstance.handleRedirectPromise` sprawdza, czy odpowiedź z przekierowania po uwierzytelnieniu jest dostępna i obsługuje ją za pomocą `handleResponse`.

4. **Logowanie i wylogowanie**:
    - Po kliknięciu przycisku login/logout `loginButton` odpowiednia funkcja (logowanie lub wylogowanie) jest wywoływana.
    - `msalInstance.loginPopup` uruchamia popup logowania, a po pomyślnym logowaniu wywołuje `handleResponse`.

5. **Uzyskiwanie tokenu i wysyłanie wiadomości**:
    - Po kliknięciu przycisku `sendButton` wysyłane jest zapytanie do API chatbota.
    - `msalInstance.acquireTokenSilent` używa istniejącej sesji do uzyskania tokenu dostępu.
    - Token dostępu jest używany w nagłówku `Authorization` przy wysyłaniu zapytania do backendu `/chat`.
    - Odpowiedź od backendu jest wyświetlana w oknie czatu.

6. **Wstrzykiwanie `clientId` i `tenantId` do frontendu**:
    - `clientId` i `tenantId` są przekazywane do frontendu jako zmienne środowiskowe zdefiniowane w App Service i umieszczone w pliku JavaScript jako wartości `clientId` i `tenantId` używane w konfiguracji MSAL.js.

```html
<script>
    const clientId = "{{ client_id }}";
    const tenantId = "{{ tenant_id }}";
</script>
```

#### Backend (`app.py`)

W pliku `app.py` jest funkcja odpowiedzialna za wstrzykiwanie `clientId` i `tenantId` do frontendu:

```python
@app.route('/')
def index():
    client_id = os.getenv('CLIENT_ID')
    tenant_id = os.getenv('TENANT_ID')
    return render_template('index.html', client_id=client_id, tenant_id=tenant_id)
```

Ta funkcja pobiera wartości `clientId` i `tenantId` z zmiennych środowiskowych i przekazuje je do szablonu `index.html`, gdzie są używane w konfiguracji MSAL.js.

1. **Obsługa zapytań do chatbota**:
    - Backend nasłuchuje na endpointzie `/chat`.
    - Każde zapytanie jest uwierzytelniane za pomocą tokenu Bearer przesyłanego w nagłówku.

2. **Weryfikacja tokenu**:
    - Backend weryfikuje token dostępu używając kodu z katalogu `helpers`.
    - Token jest dekodowany, a informacje w nim zawarte (takie jak identyfikator użytkownika i role) są używane do autoryzacji zapytania.

3. **Przetwarzanie zapytania**:
    - Po pomyślnej weryfikacji tokenu backend przetwarza zapytanie użytkownika.
    - Generowana jest odpowiedź przez model chatbota i zwracana do klienta.

4. **Dekorator sprawdzający token**:
    - W kodzie backendu używany jest dekorator `@requires_jwt_authorization`, który korzysta z kodu w katalogu `helpers` do sprawdzenia tokenu dostępu w każdym zapytaniu. Ten dekorator zapewnia, że tylko uwierzytelnieni użytkownicy mogą uzyskać dostęp do endpointu `/chat`.

### Podsumowanie

Wykonując powyższe kroki, skonfigurujesz aplikację chatbota do uwierzytelniania użytkowników za pomocą Entra ID (Azure AD), używając authorization code flow with PKCE. Zapewni to bezpieczne i skalowalne uwierzytelnianie w Twojej aplikacji.

- **Frontend** używa MSAL.js do zarządzania sesjami użytkownika, logowania i uzyskiwania tokenów dostępu.
- **Backend** weryfikuje tokeny dostępu za pomocą dekoratora `@requires_jwt_authorization`, który korzysta z kodu w katalogu `helpers`, i autoryzuje zapytania, zapewniając, że tylko uwierzytelnieni użytkownicy mogą korzystać z API chatbota.
- Proces uwierzytelniania i autoryzacji jest w pełni zintegrowany, co zapewnia bezpieczny dostęp do aplikacji chatbota.
