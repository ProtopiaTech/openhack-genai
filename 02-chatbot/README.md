# Zadanie 2: Tworzenie prostego chatbota z wykorzystaniem Azure OpenAI i LangChain

## Opis
Celem tego zadania jest stworzenie prostego chatbota, który będzie podpięty do instancji Azure OpenAI przy użyciu biblioteki LangChain. Aplikacja ma być wdrożona na usługę Azure App Service. W szczególności będziesz musiał zaimplementować endpoint `/chat`, który będzie obsługiwał komunikację z modelem językowym.

W katalogu `src` znajduje się wstępny kod, który zawiera aplikację Flask oraz kod front-endu napisany z wykorzystaniem Tailwind CSS i czystego JavaScriptu. Możesz rozszerzyć tę przykładową aplikację, aby spełnić wymagania zadania.

Należy również użyć Managed Identity, aby uzyskać podejście passwordless/secretless. Managed Identity umożliwia aplikacji automatyczne uwierzytelnianie w innych usługach Azure bez konieczności przechowywania haseł czy tajnych kluczy w kodzie, co zwiększa bezpieczeństwo i ułatwia zarządzanie dostępem.

Dodatkowo, musisz przetestować działanie content filters. Content filters służą do monitorowania i filtrowania nieodpowiednich treści generowanych przez model językowy, zapewniając, że odpowiedzi są zgodne z polityką firmy lub regulacjami prawnymi.

## Cele zadania

1. **Implementacja chatbota**:
   - Stworzenie aplikacji Flask z endpointem `/chat`, który będzie odbierał zapytania w formacie JSON i przesyłał je do Azure OpenAI za pomocą LangChain.
   - Konfiguracja aplikacji do komunikacji z Azure OpenAI, aby chatbot mógł generować odpowiedzi na podstawie zapytań użytkowników.
   - Przykładowy input:
     ```json
     {
       "message": "pytanie do llm"
     }
     ```
   - Przykładowy output:
     ```json
     {
       "content": "odpowiedz z llm",
       "response_metadata": "tu maja być metadane odpowiedz z llm"
     }
     ```
   - Front-end aplikacji, znajdujący się w katalogu `src`, obsługuje wysyłanie zapytań do endpointu `/chat` oraz wyświetlanie odpowiedzi użytkownikowi.

2. **Użycie Managed Identity**:
   - Konfiguracja Managed Identity dla Azure App Service w celu uzyskania podejścia passwordless/secretless. Managed Identity umożliwia aplikacji bezpieczne uwierzytelnianie w innych usługach Azure bez konieczności przechowywania haseł czy tajnych kluczy, co zwiększa bezpieczeństwo i upraszcza zarządzanie dostępem.

3. **Wdrożenie aplikacji**:
   - Wdrożenie aplikacji Flask na usługę Azure App Service, aby była dostępna publicznie i mogła obsługiwać zapytania użytkowników.
   - Konfiguracja Azure App Service, w tym ustawienie odpowiednich zmiennych środowiskowych i zarządzanie uprawnieniami dostępu.

4. **Testowanie i filtrowanie treści**:
   - Przetestowanie działania content filters, aby zapewnić, że chatbot nie generuje nieodpowiednich treści. Content filters służą do monitorowania i filtrowania treści, aby odpowiedzi były zgodne z polityką firmy lub regulacjami prawnymi.

## Przydatne informacje

### Wykorzystanie wiedzy z poprzednich zadań

Pamiętaj o wykorzystaniu wiedzy z poprzednich zadań. W poprzednich zadaniach znajdziesz informacje, które są pomocne w rozwiązaniu tego zadania.

### Wdrożenie aplikacji
Aplikację możesz wdrożyć bez implementacji endpointu `/chat`, żeby zobaczyć, że działa.

### Wybór rozmiaru App Service
Przy tworzeniu App Service wybierz typ Linux oraz rozmiar P1v3, który przyspieszy działanie.

### Ustawienie zmiennych środowiskowych
W katalogu `src` znajduje się skrypt `set_env.sh` do ustawiania zmiennych środowiskowych App Service z pliku `.env`. Aby go użyć, wykonaj następujące kroki:
1. Upewnij się, że masz plik `.env` z odpowiednimi zmiennymi środowiskowymi.
2. Ustaw zmienne środowiskowe `RESOURCE_GROUP` oraz `WEBAPP_NAME`:
   ```bash
   export RESOURCE_GROUP="TwojaNazwaResourceGroup"
   export WEBAPP_NAME="TwojaNazwaWebApp"
   ```
3. Wykonaj skrypt `set_env.sh`:
   ```bash
   ./set_env.sh
   ```

### Wdrażanie aplikacji
Do wdrażania aplikacji możesz użyć następujących poleceń:
1. Spakuj kod do pliku zip:
   ```bash
   zip -r myapp.zip .
   ```
2. Ustaw zmienne środowiskowe `RESOURCE_GROUP` oraz `WEBAPP_NAME`:
   ```bash
   export RESOURCE_GROUP="TwojaNazwaResourceGroup"
   export WEBAPP_NAME="TwojaNazwaWebApp"
   ```
3. Wgraj plik zip za pomocą Azure CLI:
   ```bash
   az webapp deploy --resource-group $RESOURCE_GROUP --name $WEBAPP_NAME --src-path myapp.zip
   ```

## Jak można to zaimplementować?

> ## Użyj [langchain](https://www.langchain.com/) do realizacji zadania

### 1. Uruchomienie aplikacji lokalnie i wdrożenie wstępnej wersji

Aby rozpocząć pracę nad aplikacją, uruchom ją lokalnie i wdroż wstępną wersję na Azure App Service. Skorzystaj z poniższych linków, aby uzyskać szczegółowe instrukcje:

- [Quickstart: Deploy a Python (Flask) web app to Azure](https://learn.microsoft.com/en-us/azure/app-service/quickstart-python?tabs=flask%2Cwindows%2Cazure-cli%2Cazure-cli-deploy%2Cdeploy-instructions-azportal%2Cterminal-bash%2Cdeploy-instructions-zip-azcli)
- [Azure CLI Web App Deploy Command](https://learn.microsoft.com/en-us/cli/azure/webapp?view=azure-cli-latest#az-webapp-deploy)

### 2. Rozszerzenie endpointu `/chat`

Rozszerz endpoint `/chat`, aby obsługiwał zapytania do Azure OpenAI za pomocą LangChain. Wykorzystaj wiedzę z zadania 1 oraz dokumentację:

- [LangChain Azure Chat OpenAI Integration](https://python.langchain.com/v0.2/docs/integrations/chat/azure_chat_openai/)

### 3. Włącz Managed Identity na App Service

Skonfiguruj Managed Identity dla App Service, aby uzyskać dostęp do Azure OpenAI bez użycia haseł lub kluczy tajnych. Więcej informacji znajdziesz tutaj:

- [Azure App Service Managed Identity](https://learn.microsoft.com/en-us/azure/app-service/overview-managed-identity?tabs=portal%2Chttp)

### 4. Nadaj uprawnienia dla tożsamości App Service do dostępu do Azure OpenAI

Upewnij się, że Managed Identity ma odpowiednie uprawnienia do dostępu do Azure OpenAI. Skorzystaj z poniższych linków, aby dowiedzieć się, jak przypisać role:

- [Role-Based Access Control for Azure OpenAI](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/role-based-access-control)
- [Assign Azure Roles using the Azure Portal](https://learn.microsoft.com/en-us/azure/role-based-access-control/role-assignments-portal)

### 5. Ustaw zmienne środowiskowe (configuration) w App Service

Skonfiguruj zmienne środowiskowe w Azure App Service, aby aplikacja mogła korzystać z odpowiednich ustawień i poświadczeń. Więcej informacji znajdziesz tutaj:

- [Configure App Settings in Azure App Service](https://learn.microsoft.com/en-us/azure/app-service/configure-common?tabs=portal)

### 6. Wdrożenie aplikacji

Korzystaj z sekcji [Przydatne informacje](#przydatne-informacje) lub instrukcji z zadania 1, aby poprawnie wdrożyć aplikację, ustawić zmienne środowiskowe i skonfigurować Managed Identity.

### 7. Przetestuj content filters

Przetestuj działanie content filters, aby upewnić się, że chatbot nie generuje nieodpowiednich treści. Zapytaj mentora, aby uzyskać przykłady promptów do testowania filtrów treści.
