# Zadanie 1: Ładowanie danych i ich klasyfikacja

## Opis

Twoim zadaniem jest przygotowanie procesu ładowania danych do Azure AI Search oraz wykonanie klasyfikacji załadowanych dokumentów. Dokumenty te mogą być klasyfikowane jako "Dane osobowe", "Prywatny" lub "Publiczny". Klasyfikacja musi być zapisana w polu typu "filterable", aby umożliwić użycie filtrów bezpieczeństwa (Security Filters) w Azure AI Search. Przykładowe pliki PDF znajdują się w katalogu `../data`.

Podczas klasyfikacji użyj angielskich nazw w formacie przyjaznym dla programowania: `personal-data` dla "Dane osobowe", `private` dla "Prywatny", oraz `public` dla "Publiczny". W kolejnym zadaniu zespół skorzysta z Security Filters, aby ograniczyć dostęp do dokumentów na podstawie ich klasyfikacji.

Po przeprocesowaniu dokumentów, należy je przenieść do odpowiednich kontenerów: `personal-data`, `private` lub `public`, w celu archiwizacji lub dalszego przetwarzania. Upewnij się, że te kontenery zostały utworzone przed rozpoczęciem procesu.

## Przydatne informacje

### Skrypt upload.sh

Do wgrywania danych do Azure Storage można użyć skryptu `upload.sh`. Skrypt ten automatycznie przesyła pliki z lokalnego katalogu do odpowiednich kontenerów w Azure Storage, zgodnie z klasyfikacją dokumentów. Upewnij się, że masz zainstalowane narzędzie Azure CLI i zaloguj się do swojego konta Azure przed uruchomieniem skryptu.

### Przykładowa struktura skryptu

W katalogu zadania znajduje się **przykładowa** struktura kodu w pliku `main.py`.

Funkcja `__main__` zawiera przykładową kolejność wywołań niżej opisanych funkcji.

**Nie musisz korzystać z tego pliku. Jest tylko wskazówką.**

### Przykładowy plik .env

Przykładowy plik `.env` powinien zawierać następujące informacje:

```bash
STORAGE_ACCOUNT_NAME=""
STORAGE_CONTAINER_NAME_IN="data-in"
AZURE_OPENAI_API_VERSION="2023-12-01-preview"
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_CHAT_DEPLOYMENT_NAME="" 
AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT=""
AZURE_AI_SEARCH_ENDPOINT=""
INDEX_NAME=""
```

Uzupełnij go swoimi wartościami ze środowsika.

Aby załadować zmienne środowiskowe z pliku `.env` w Pythonie, możesz użyć biblioteki `python-dotenv`. Oto przykład kodu:

```python
from dotenv import load_dotenv
import os

load_dotenv()

storage_account_name = os.getenv('AZURE_STORAGE_ACCOUNT')
search_service_name = os.getenv('AZURE_AI_SEARCH_ENDPOINT')

print(storage_account_name, search_service_name)
```

## Cele zadania

1. **Konfiguracja indeksu**:
   - Stworzenie i skonfigurowanie indeksu w Azure AI Search, który będzie zawierał odpowiednie pola do przechowywania informacji o dokumentach oraz ich klasyfikacji.
   - Dodanie pola typu `filterable` do indeksu, które będzie przechowywało informacje o klasyfikacji dokumentu.

2. **Załadowanie dokumentów i klasyfikacja**:
   - Przygotowanie procesu ładowania plików PDF do Azure AI Search.
   - Klasyfikacja każdego dokumentu na podstawie jego treści jako "Dane osobowe", "Prywatny" lub "Publiczny".
   - Zapisanie klasyfikacji w polu typu "filterable" podczas ładowania dokumentów do Azure AI Search.
   - W ten sposób załadujesz dane oraz dokonasz ich klasyfikacji w jednym kroku, co uprości cały proces i zapewni spójność danych.

3. **Przeniesienie dokumentów po przeprocesowaniu**:
   - Po zakończeniu procesu ładowania i klasyfikacji, dokumenty należy przenieść do odpowiednich kontenerów: `personal-data`, `private` lub `public`, w celu archiwizacji lub dalszego przetwarzania. Upewnij się, że te kontenery zostały utworzone przed rozpoczęciem procesu.

## Jak można to zaimplementować?

> ## Kod ładujący dokumenty i klasyfikujący może być uruchamiany lokalnie z GitHub Codespace.
> 
> ## Użyj  [langchain](https://www.langchain.com/) do realizacji zadania


### Logika główna

Aby zaimplementować proces ładowania danych do Azure AI Search oraz ich klasyfikację, należy wykonać kilka kroków:

1. **Stworzenie i konfiguracja indeksu**:
   - Skonfigurować indeks w Azure AI Search z odpowiednimi polami, w tym polem `filterable` do przechowywania klasyfikacji dokumentów.

2. **Ładowanie i klasyfikacja dokumentów**:
   - Przygotować proces ładowania plików PDF do Azure AI Search.
   - Wykonać klasyfikację dokumentów na podstawie ich treści.
   - Zapisanie klasyfikacji w polu "filterable" podczas ładowania dokumentów.

### Funkcje do zaimplementowania

#### Funkcja `get_vector_store`

- **Opis**: Ta funkcja konfiguruje i zwraca indeks wektorowy Azure AI Search, który może być używany do wyszukiwania wektorowego i filtrowania dokumentów.
- **Argumenty wejściowe**:
  - `connection_string`: Connection string do Azure AI Search.
  - `index_name`: Nazwa indeksu, który ma zostać utworzony lub użyty.
- **Zadania**:
  - Konfiguracja indeksu z odpowiednimi polami, w tym pola typu "filterable" do przechowywania klasyfikacji dokumentów.
  - Utworzenie klienta indeksu Azure AI Search.
  - Zwrócenie skonfigurowanego klienta indeksu do dalszego użycia.

```python
def get_vector_store(connection_string, index_name):
    # Logika tworzenia i konfigurowania indeksu wektorowego w Azure AI Search
    pass
```

##### Tips & tricks

- [Azure Identity client library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#authenticate-with-defaultazurecredential)
- Utwórz model typu embedding (`text-embedding-3-large`) w Azure OpenAI - [link](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model).
- Użycie [Azure AI Search w langchain](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/)
- [API langchain dla AI Serach](https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.azuresearch.AzureSearch.html#langchain_community.vectorstores.azuresearch.AzureSearch)
- Uwierzytelnianie z wykorzystaniem Azure AD
  ```python
  vector_store: AzureSearch = AzureSearch(
    azure_search_endpoint=os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
    azure_search_key=None,
    index_name=index_name,
    embedding_function=embeddings.embed_query,
    fields=fields
  )
  ```
- `azure_search_key=None` wymusza logowanie z Azure AD.
- Tworzenie embeddings z wykorzystaniem Azure AD

  ```python
  embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
    azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"),
    openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider
  )
  ```

- Utwórz własny indeks z korzystając z domyślmych pól (`id`,`content`,`content_vector`,`metadata`,`title`,`source`) oraz dodaj własne na potrzeby  `data_classification`. [Create a new index with custom filterable fields](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/#create-a-new-index-with-custom-filterable-fields)

#### Funkcja `list_blobs`
- **Opis**: Ta funkcja zwraca listę blobów w kontenerze.
- **Argumenty wejściowe**:
  - `account_name`: Nazwa konta Azure Storage.
  - `container_name`: Nazwa kontenera.
  - `credential`: Poświadczenia do uwierzytelnienia.
- **Zadania**:
  - Połączenie z Azure Blob Storage.
  - Wylistowanie i zwrócenie wszystkich blobów w podanym kontenerze.

```python
def list_blobs(account_name, container_name, credential):
    # Logika listowania blobów w Azure Blob Storage
    pass
```

##### Tips & tricks

- [Azure Identity client library for Python](https://learn.microsoft.com/en-us/python/api/overview/azure/identity-readme?view=azure-python#authenticate-with-defaultazurecredential)
- [Quickstart: Azure Blob Storage client library for Python](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli&pivots=blob-storage-quickstart-scratch)

#### Funkcja `get_blob_content`

- **Opis**: Ta funkcja zwraca zawartość określonego bloba.
- **Argumenty wejściowe**:
  - `account_name`: Nazwa konta Azure Storage.
  - `container_name`: Nazwa kontenera.
  - `blob_name`: Nazwa bloba.
  - `credential`: Poświadczenia do uwierzytelnienia.
- **Zadania**:
  - Połączenie z Azure Blob Storage.
  - Pobranie i zwrócenie zawartości bloba.

```python
def get_blob_content(account_name, container_name, blob_name, credential):
    # Logika pobierania zawartości bloba
    pass
```
##### Tips & tricks

- [Quickstart: Azure Blob Storage client library for Python](https://learn.microsoft.com/en-us/azure/storage/blobs/storage-quickstart-blobs-python?tabs=managed-identity%2Croles-azure-portal%2Csign-in-azure-cli&pivots=blob-storage-quickstart-scratch)

#### Funkcja `save_blob_to_temp_file`
- **Opis**: Ta funkcja zapisuje zawartość bloba do tymczasowego pliku.
- **Argumenty wejściowe**:
  - `blob_content`: Zawartość bloba.
- **Zadania**:
  - Zapisanie zawartości bloba do tymczasowego pliku.
  - Zwrócenie ścieżki do tymczasowego pliku.

```python
def save_blob_to_temp_file(blob_content):
    # Logika zapisywania zawartości bloba do tymczasowego pliku
    pass
```

##### Tips & tricks

- Użyj gotowej metody `tempfile.NamedTemporaryFile`.

#### Funkcja `get_file_classification`

- **Opis**: Ta funkcja klasyfikuje dokument jako `personal-data`, `private` lub `public`.
- **Argumenty wejściowe**:
  - `credential`: Poświadczenia do uwierzytelnienia.
  - `file_path`: Ścieżka do pliku PDF.
- **Zadania**:
  - Analiza zawartości pliku PDF.
  - Klasyfikacja dokumentu na podstawie zawartości.
  - Zwrócenie klasyfikacji.

```python
def get_file_classification(credential, file_path):
    # Logika klasyfikacji pliku PDF
    pass
```

##### Tips & tricks

- Użyj [langchain](https://www.langchain.com/)
- Do pracy musisz wdrożyć model na swojej instacji OpenAI - [link](https://learn.microsoft.com/en-us/azure/ai-services/openai/how-to/create-resource?pivots=web-portal#deploy-a-model).
- Skorzystaj z Summarize w LangChain z podejściem Map-Reduce - [link](https://python.langchain.com/v0.2/docs/tutorials/summarization/#map-reduce).
- Ładowanie PDF w LangChain - [How to load PDFs - Using PyPDF](https://python.langchain.com/v0.2/docs/how_to/document_loader_pdf/#using-pypdf). Ładując zamist `pages` użyj zmiennej `docs`.
- Do łączenia się z Azure OpenAI użyj uwierzytelniania z Azure AD:
  
  ```python
  token_provider = get_bearer_token_provider(
    credential, "https://cognitiveservices.azure.com/.default"
  )
  llm = AzureChatOpenAI(
    openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
    azure_ad_token_provider=token_provider
  )
  ```

- [AzureChatOpenAI](https://python.langchain.com/v0.2/docs/integrations/chat/azure_chat_openai/)
- [AzureChatOpenAI Lib](https://api.python.langchain.com/en/latest/chat_models/langchain_openai.chat_models.azure.AzureChatOpenAI.html)
- [Azure Active Directory Authentication](https://python.langchain.com/v0.2/docs/integrations/llms/azure_openai/#azure-active-directory-authentication)
- Pisząc prompt dla funkcji Map, poinstruuj, aby LLM dokonał klasyfikacji dokumentów. Podaj, co ma zrobić, jeśli nie będzie wiedział, jak sklasyfikować dokument.
- Pisząc prompt dla funkcji Reduce, określ kolejność klasyfikacji, czyli która ma najwyższy priorytet.
- [Introduction to prompt engineering](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/prompt-engineering)
- [Prompt engineering techniques](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/advanced-prompt-engineering?pivots=programming-language-chat-completions)
- [System message framework and template recommendations for Large Language Models (LLMs)](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/system-message)

#### Funkcja `add_document_to_vector_store`

- **Opis**: Ta funkcja dodaje dokument do Azure AI Search z odpowiednią klasyfikacją.
- **Argumenty wejściowe**:
  - `vector_store`: Instancja sklepu wektorowego.
  - `file_path`: Ścieżka do pliku PDF.
  - `data_classification`: Klasyfikacja dokumentu.
  - `title`: Tytuł dokumentu.
  - `source`: Źródło dokumentu.
- **Zadania**:
  - Przetworzenie pliku PDF.
  - Dodanie dokumentu do sklepu wektorowego wraz z jego klasyfikacją.

```python
def add_document_to_vector_store(vector_store, file_path, data_classification, title, source):
    # Logika dodawania dokumentu do Azure AI Search
    pass
```

##### Tips & tricks

- Użycie [Azure AI Search w langchain](https://python.langchain.com/v0.2/docs/integrations/vectorstores/azuresearch/)
- [API langchain dla AI Serach](https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.azuresearch.AzureSearch.html#langchain_community.vectorstores.azuresearch.AzureSearch)
- Uzupełnienie dodatkowych pól w indeksie (`metadata`, `title`, `source`, `data_classification`). Jest to słabo udokumentowane.
  ```python
  for doc in docs:
    doc.metadata["data_classification"] = data_classification
    doc.metadata["title"] = title
    doc.metadata["source"] = source
  ```
- Jako `title` ustaw nazwę pliku w blob
- Jako `source` przygotuj url do blob w nowej lokalizacji po przeprocesowaniu.
  ```python
  source=f"https://{account_name}.blob.core.windows.net/{data_classification}/{blob.name}"
  ```
- Ładowanie PDF w LangChain - [How to load PDFs - Using PyPDF](https://python.langchain.com/v0.2/docs/how_to/document_loader_pdf/#using-pypdf). Ładując zamist `pages` użyj zmiennej `docs`.

#### Funkcja `move_blob`

- **Opis**: Ta funkcja przenosi bloba do nowego kontenera lub katalogu na podstawie klasyfikacji.
- **Argumenty wejściowe**:
  - `account_name`: Nazwa konta Azure Storage.
  - `container_name`: Nazwa kontenera.
  - `data_classification`: Klasyfikacja dokumentu.
  - `blob_name`: Nazwa bloba.
  - `credential`: Poświadczenia do uwierzytelnienia.
- **Zadania**:
  - Przeniesienie bloba do nowej lokalizacji na podstawie klasyfikacji.

```python
def move_blob(account_name, container_name, data_classification, blob_name, credential):
    # Logika przenoszenia bloba w Azure Blob Storage
    pass
```

#### Tips & tricks

- Do przeniesienia wykorzystaj `start_copy_from_url` z [BlobClient](https://learn.microsoft.com/en-us/python/api/azure-storage-blob/azure.storage.blob.blobclient?view=azure-python)
- Po skopiowaniu skasuj `delete_blob()` korzystając z `BlobClient`.
- Poczekaj na skopiowanie pliku przed kasowaniem.

  ```python
  destination_blob_client.start_copy_from_url(source_blob_client.url)
  props = destination_blob_client.get_blob_properties()
  while props.copy.status == "pending":
    props = destination_blob_client.get_blob_properties()
  if props.copy.status != "success":
    raise Exception(f"Copy failed with status: {props.copy.status}")
  source_blob_client.delete_blob()
  ```
