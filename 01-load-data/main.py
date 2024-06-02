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


# Get content of blob
def get_blob_content(account_name, container_name, blob_name, credential):
    print(f"Get content of blob {blob_name}")

# Save content of blob to temp file
def save_blob_to_temp_file(blob_content):
    print(f"Save blob to temp file")

# Move blob to another container
def move_blob(account_name, source_container_name, destination_container_name, blob_name, credential):
    print(f"Moving blob '{blob_name}' from '{source_container_name}' to '{destination_container_name}'.")    

    print(f"Blob '{blob_name}' has been moved from '{source_container_name}' to '{destination_container_name}'.")

# Proceed pdf blob with MapReduceDocumentsChain, use blob content as input
def get_file_classification(credential, temp_pdf_path):
    print("Proceed pdf blob with MapReduceDocumentsChain, use blob content as input")

def get_vector_store(credential, index_name):
    print("Get vector store")

def add_document_to_vector_store(vector_store, file_path, data_classification, title, source):
    print("Add document '{title}' to vector store")

if __name__ == "__main__":
    load_dotenv()
    account_name = os.getenv("STORAGE_ACCOUNT_NAME")
    container_name = os.getenv("STORAGE_CONTAINER_NAME_IN")
    credential = DefaultAzureCredential()
    index_name = os.getenv("INDEX_NAME")
    # Przykładowa implementacja
    # vector_store = get_vector_store(credential, "index_name")
    # blobs = list_blobs(account_name, container_name, credential)
    # for blob in blobs:
    #     blob_content = get_blob_content(account_name, container_name, blob.name, credential)
    #     file_path = save_blob_to_temp_file(blob_content)
    #     data_classification = get_file_classification(credential, file_path)
    #     add_document_to_vector_store(
    #         vector_store=vector_store,
    #         file_path=file_path,
    #         data_classification=data_classification,
    #         title=blob.name,
    #         source=f"https://{account_name}.blob.core.windows.net/{data_classification}/{blob.name}"
    #     )
    #     move_blob(account_name, container_name, data_classification, blob.name, credential)
