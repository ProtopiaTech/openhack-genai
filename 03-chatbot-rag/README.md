# Zadanie 3: Rozszerzenie Chatbota o RAG

## Opis
Celem tego zadania jest rozszerzenie istniejącej aplikacji Chatbot o funkcjonalność Retrieval-Augmented Generation (RAG). W ramach zadania, wykorzystasz dane załadowane i sklasyfikowane w zadaniu 1 oraz integrację z Azure OpenAI z zadania 2. RAG łączy modele generacyjne (jak GPT) z mechanizmami wyszukiwania (jak wektoryzacja dokumentów i wyszukiwanie wektorowe) w celu dostarczania bardziej precyzyjnych i kontekstowych odpowiedzi. W tym zadaniu będziemy wykorzystywać chain z biblioteki LangChain, aby połączyć proces wyszukiwania i generowania odpowiedzi w spójny workflow.

## Cele zadania

1. **Integracja z Azure AI Search**:
   - Skonfigurowanie integracji aplikacji Chatbot z Azure AI Search, aby umożliwić wyszukiwanie dokumentów na podstawie zapytań użytkowników.
   - Wykorzystanie funkcji wektorowych Azure AI Search do znajdowania najbardziej trafnych dokumentów na podstawie zapytań.

2. **Implementacja Retrieval-Augmented Generation (RAG)**:
   - Rozszerzenie endpointu `/chat` o funkcjonalność RAG.
   - Implementacja logiki wyszukiwania dokumentów w Azure AI Search przed generowaniem odpowiedzi przez model językowy.
   - Łączenie wyników wyszukiwania z wygenerowaną odpowiedzią w celu dostarczania bardziej trafnych i szczegółowych informacji.

3. **Wdrożenie i testowanie**:
   - Wdrożenie rozszerzonej aplikacji na usługę Azure App Service.
   - Przeprowadzenie testów w celu zapewnienia poprawnego działania funkcji RAG.

## Przydatne informacje

### Wykorzystanie wiedzy z poprzednich zadań

Pamiętaj o wykorzystaniu wiedzy z poprzednich zadań. W zadaniu 1 nauczyłeś się, jak ładować i klasyfikować dokumenty w Azure AI Search. Te umiejętności są kluczowe dla przygotowania danych, które będą używane w funkcjonalności RAG. W zadaniu 2 zdobyłeś doświadczenie w tworzeniu prostego chatbota z wykorzystaniem Azure OpenAI i LangChain, co stanowi podstawę do rozszerzenia funkcjonalności o RAG.

W szczególności, ważne jest, aby:
- Używać wcześniej skonfigurowanych indeksów i klasyfikacji dokumentów z zadania 1.
- Wykorzystać istniejący endpoint `/chat` jako punkt wyjścia do dodania funkcji RAG.
- Skorzystać z wiedzy na temat Managed Identity do bezpiecznego uwierzytelniania i autoryzacji w usługach Azure.

Dzięki temu podejściu będziesz mógł efektywnie połączyć wszystkie elementy i stworzyć zaawansowanego chatbota, który będzie mógł dostarczać precyzyjne i kontekstowe odpowiedzi na zapytania użytkowników.

## Jak można to zaimplementować?

Implementacja RAG w aplikacji Chatbot wymaga kilku kroków. Przede wszystkim, musisz skonfigurować Azure AI Search jako vector store, co pozwoli na wyszukiwanie dokumentów na podstawie zapytań użytkowników. Następnie, zaimplementujesz mechanizm Retrieval-Augmented Generation, który łączy wyszukiwanie i generowanie odpowiedzi w jeden spójny proces. Na końcu wdrożysz i przetestujesz aplikację, aby upewnić się, że wszystkie elementy działają poprawnie.

Do implementacji RAG możesz użyć następujących źródeł wiedzy:
- [LangChain RAG Tutorial](https://python.langchain.com/v0.2/docs/tutorials/rag/)
- [LangChain QA Chat History Tutorial](https://python.langchain.com/v0.2/docs/tutorials/qa_chat_history/)

### Krok 1: Konfiguracja AzureSearch jako Vector Store
Pierwszym krokiem jest skonfigurowanie Azure AI Search jako vector store. W tym celu, wykorzystasz wiedzę z zadania 1, gdzie nauczyłeś się, jak tworzyć i konfigurować indeksy oraz ładować dane do Azure AI Search. Wykorzystaj te same metody i rozszerz je o funkcjonalności potrzebne do RAG.

### Krok 2: Implementacja Retrieval-Augmented Generation (RAG)
Następnie, zaimplementuj funkcjonalność RAG. Użyj metody `as_retriever` na vector store, aby skonfigurować mechanizm wyszukiwania. Metoda ta pozwala na zdefiniowanie typu wyszukiwania (`search_type`), który może być `similarity`, `hybrid`, lub `semantic_hybrid`.

<KOD>
retriever = vector_store.as_retriever(
    search_type="hybrid",
)
</KOD>

Dodatkowe zasoby:
- [Vector Similarity Search with AzureSearch](https://python.langchain.com/v0.1/docs/integrations/vectorstores/azuresearch/#perform-a-vector-similarity-search)
- [AzureSearch API Documentation](https://api.python.langchain.com/en/latest/vectorstores/langchain_community.vectorstores.azuresearch.AzureSearch.html)
- [Azure Cognitive Search and LangChain Integration](https://techcommunity.microsoft.com/t5/ai-azure-ai-services-blog/azure-cognitive-search-and-langchain-a-seamless-integration-for/ba-p/3901448)

### Krok 3: Rozszerzenie Endpointu `/chat`
Rozszerz endpoint `/chat`, aby wykorzystać nowo skonfigurowany retriever. Endpoint ten będzie najpierw wyszukiwał odpowiednie dokumenty, a następnie generował odpowiedź na podstawie wyników wyszukiwania.

### Krok 4: Wdrożenie i Testowanie
Wdrożenie aplikacji na usługę Azure App Service jest ostatnim krokiem. Upewnij się, że wszystkie komponenty są poprawnie skonfigurowane i przetestowane. Przeprowadź testy, aby zweryfikować, że aplikacja poprawnie integruje wyszukiwanie dokumentów i generowanie odpowiedzi.
