# Import the necessary module
from importlib import metadata
import io
import os
import tempfile
from azure.storage.blob import BlobServiceClient
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain
from langchain.chains import StuffDocumentsChain, ReduceDocumentsChain, MapReduceDocumentsChain, LLMChain
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_text_splitters import CharacterTextSplitter
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)

# List blob and return the list of blobs
def list_blobs(account_name, container_name, credential):
    print(f"List blobs in container {container_name}")
    blob_list = []
    try:
        # Define the blob_service_client variable
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )
        container_client = blob_service_client.get_container_client(container_name)
        blobs = container_client.list_blobs()
        for blob in blobs:
            blob_list.append(blob)
            print(blob.name)
    except Exception as e:
        print(e)
    return blob_list

# Get content of blob
def get_blob_content(account_name, container_name, blob_name, credential):
    print(f"Get content of blob {blob_name}")
    try:
        # Define the blob_service_client variable
        blob_service_client = BlobServiceClient(
            account_url=f"https://{account_name}.blob.core.windows.net",
            credential=credential
        )
        container_client = blob_service_client.get_container_client(container_name)
        blob_client = container_client.get_blob_client(blob_name)
        blob_content = blob_client.download_blob().readall()
        return blob_content
    except Exception as e:
        print(e)

# Save content of blob to temp file
def save_blob_to_temp_file(blob_content):
    with tempfile.NamedTemporaryFile(delete=False) as temp_pdf:
        temp_pdf.write(blob_content)
        temp_pdf_path = temp_pdf.name
    return temp_pdf_path

# Move blob to another container
def move_blob(account_name, source_container_name, destination_container_name, blob_name, credential):
    blob_service_client = BlobServiceClient(
        account_url=f"https://{account_name}.blob.core.windows.net",
        credential=credential
    )
    source_container_client = blob_service_client.get_container_client(source_container_name)
    destination_container_client = blob_service_client.get_container_client(destination_container_name)
    source_blob_client = source_container_client.get_blob_client(blob_name)
    destination_blob_client = destination_container_client.get_blob_client(blob_name)
    
    destination_blob_client.start_copy_from_url(source_blob_client.url)
    props = destination_blob_client.get_blob_properties()
    while props.copy.status == "pending":
        props = destination_blob_client.get_blob_properties()
    
    if props.copy.status != "success":
        raise Exception(f"Copy failed with status: {props.copy.status}")
    source_blob_client.delete_blob()
    print(f"Blob '{blob_name}' has been moved from '{source_container_name}' to '{destination_container_name}'.")

# Proceed pdf blob with MapReduceDocumentsChain, use blob content as input
def get_file_classification(credential, temp_pdf_path):
    # Load the PDF file
    loader = PyPDFLoader(temp_pdf_path)
    docs = loader.load_and_split()
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    llm = AzureChatOpenAI(
        openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
        azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
        azure_ad_token_provider=token_provider
    )

    map_template = """The following is a set of documents
    {docs}
    Twoim zadaniem jest sklasyfikować dokument. Klasyfikacja dokumentów od najważniejszego do najniższego: Dane osobowe, Prywatny, Publiczny.
    Użyj następujących etykiet: personal-data dla "Dane osobowe", private dla "Prywatny", oraz public dla "Publiczny"
    Jeżeli nie jest możliwe sklasyfikowanie usatw etykietę `private`.
    W odpowiedzi podaj tylko klasyfikację. Jeżeli nie jesteś pewien, użyj etykiety private.
    Classification:"""
    
    map_prompt = PromptTemplate.from_template(map_template)

    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    # Reduce
    reduce_template = """Poniżej znajduje się klasyfikacja dokumentów:
    {docs}
    Twoim zadaniem jest wybrać jedną klasyfikację dla tego zestawu. Klasyfikacja dokumentów od najważniejszego do najniższego: Dane osobowe, Prywatny, Publiczny.
    Użyj następujących etykiet: personal-data dla "Dane osobowe", private dla "Prywatny", oraz public dla "Publiczny"
    W odpowiedzi podaj tylko klasyfikację. Jeżeli nie jesteś pewien, użyj etykiety private.
    Classification:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)

    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt)

    # Takes a list of documents, combines them into a single string, and passes this to an LLMChain
    combine_documents_chain = StuffDocumentsChain(
        llm_chain=reduce_chain, document_variable_name="docs"
    )
    # Combines and iteratively reduces the mapped documents
    reduce_documents_chain = ReduceDocumentsChain(
        # This is final chain that is called.
        combine_documents_chain=combine_documents_chain,
        # If documents exceed context for `StuffDocumentsChain`
        collapse_documents_chain=combine_documents_chain,
        # The maximum number of tokens to group documents into.
        token_max=4000,
    )
    # Combining documents by mapping a chain over them, then combining results
    map_reduce_chain = MapReduceDocumentsChain(
        # Map chain
        llm_chain=map_chain,
        # Reduce chain
        reduce_documents_chain=reduce_documents_chain,
        # The variable name in the llm_chain to put the documents in
        document_variable_name="docs",
        # Return the results of the map steps in the output
        return_intermediate_steps=False,
    )
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    split_docs = text_splitter.split_documents(docs)
    return map_reduce_chain.run(split_docs)

def get_vector_store(credential, index_name):
    token_provider = get_bearer_token_provider(
        credential, "https://cognitiveservices.azure.com/.default"
    )

    # Define embedding model
    embeddings: AzureOpenAIEmbeddings = AzureOpenAIEmbeddings(
        azure_deployment=os.getenv("AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT"),
        openai_api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        azure_ad_token_provider=token_provider
    )
    embedding_function = embeddings.embed_query

    # Define fields
    fields = [
        SimpleField(name="id", type=SearchFieldDataType.String, key=True, filterable=True),
        SimpleField(name="data_classification", type=SearchFieldDataType.String, filterable=True),
        SearchableField(name="metadata",type=SearchFieldDataType.String,searchable=True,),
        SearchableField(name="title",type=SearchFieldDataType.String,searchable=True),
        SimpleField( name="source", type=SearchFieldDataType.String, filterable=True),
        SearchableField( name="content", type=SearchFieldDataType.String, searchable=True),
        SearchField(
            name="content_vector",
            type=SearchFieldDataType.Collection(SearchFieldDataType.Single),
            searchable=True,
            vector_search_dimensions=len(embedding_function("Text")),
            vector_search_profile_name="myHnswProfile",
        ),
    ]

    # Define the Azure Search vector store
    vector_store: AzureSearch = AzureSearch(
        azure_search_endpoint=os.getenv("AZURE_AI_SEARCH_ENDPOINT"),
        azure_search_key=None,
        index_name=index_name,
        embedding_function=embeddings.embed_query,
        fields=fields
    )
    return vector_store

def add_document_to_vector_store(vector_store, file_path, data_classification, title, source):
    loader = PyPDFLoader(file_path)
    documents = loader.load()
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)
    for doc in docs:
        doc.metadata["data_classification"] = data_classification
        doc.metadata["title"] = title
        doc.metadata["source"] = source
    vector_store.add_documents(
        documents=docs,
    )

if __name__ == "__main__":
    load_dotenv()
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    container_name = os.getenv("STORAGE_CONTAINER_NAME_IN")
    credential = DefaultAzureCredential()
    vector_store = get_vector_store(credential, "test111")
    blobs = list_blobs(account_name, container_name, credential)
    for blob in blobs:
        blob_content = get_blob_content(account_name, container_name, blob.name, credential)
        file_path = save_blob_to_temp_file(blob_content)
        data_classification = get_file_classification(credential, file_path)
        add_document_to_vector_store(
            vector_store=vector_store,
            file_path=file_path,
            data_classification=data_classification,
            title=blob.name,
            source=f"https://{account_name}.blob.core.windows.net/{data_classification}/{blob.name}"
        )
        move_blob(account_name, container_name, data_classification, blob.name, credential)
