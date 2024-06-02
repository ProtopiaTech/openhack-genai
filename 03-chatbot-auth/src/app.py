import json
from backoff import constant
from flask import Flask, render_template, request, jsonify
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from helpers.authorization import requires_jwt_authorization, AuthError
from langchain_community.vectorstores.azuresearch import AzureSearch
from langchain_openai import AzureOpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from azure.search.documents.indexes.models import (
    SearchableField,
    SearchField,
    SearchFieldDataType,
    SimpleField,
)

def serialize_error_details(e):
    error_details = {}
    for key, value in e.__dict__.items():
        try:
            json.dumps(value)  # Test if the value is JSON serializable
            error_details[key] = value
        except TypeError:
            error_details[key] = str(value)  # Convert non-serializable values to strings
    return error_details

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
    )
    return vector_store

# Get Azure credentials
app = Flask(__name__)

with app.app_context():
   load_dotenv()
   PUBLIC_GROUP_ID = os.environ["PUBLIC_GROUP_ID"]
   PRIVATE_GROUP_ID = os.environ["PRIVATE_GROUP_ID"]
   PERSONAL_DATA_GROUP_ID = os.environ["PERSONAL_DATA_GROUP_ID"]
   ROLES_MAPPING = {
       PUBLIC_GROUP_ID: "public",
       PRIVATE_GROUP_ID: "private",
       PERSONAL_DATA_GROUP_ID: "personal-data"
   }
   credential = DefaultAzureCredential()
   token_provider = get_bearer_token_provider(
       credential, "https://cognitiveservices.azure.com/.default"
   )
   global llm
   llm = AzureChatOpenAI(
       openai_api_version=os.environ["AZURE_OPENAI_API_VERSION"],
       azure_deployment=os.environ["AZURE_OPENAI_CHAT_DEPLOYMENT_NAME"],
       azure_ad_token_provider=token_provider
   )

#@app.errorhandler(AuthError)
#def handle_auth_error(ex):
#    response = jsonify(ex.error)
#    response.status_code = ex.status_code
#    return response

@app.route('/')
def index():
    client_id = '35b85d8b-9532-4b19-8b20-d3d19b3e0fbe'  # Replace with your Azure AD application client ID
    tenant_id = 'cc58971a-0481-4ec0-bf8d-bb2e265db003'  # Replace with your tenant ID
    return render_template('index.html', client_id=client_id, tenant_id=tenant_id)

@app.route('/chat', methods=['POST'])
@requires_jwt_authorization(roles=[PERSONAL_DATA_GROUP_ID], roles_mapping=ROLES_MAPPING)
def chat(roles):
    print(roles)
    if request.is_json:
        data = request.get_json()
        print(data)
        message = data.get('message', '')
        print(message)
        if message:
            try:
                system_prompt = (
                        "You are an assistant for question-answering tasks. "
                        "Use the following pieces of retrieved context to answer "
                        "the question. If you don't know the answer, say that you "
                        "don't know. Use three sentences maximum and keep the "
                        "answer concise."
                        "\n\n"
                        "{context}"
                  )
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])
                #response = llm.invoke(message)
                vector_store = get_vector_store(credential, "test111")
                filter_query = " or ".join([f"data_classification eq '{role}'" for role in roles])
                retriever = vector_store.as_retriever(
                    search_type="hybrid",
                    search_kwargs={
                        "filters":filter_query
                        }
                )
                print(f'retriever search_type: {retriever.search_type}')
                print(f'retriever search_kwargs: {retriever.search_kwargs}')
                #print(filter_query)
                question_answer_chain = create_stuff_documents_chain(llm, prompt)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)
                response = rag_chain.invoke({"input": message})
                print(response)
                return jsonify({
                    'content': response["answer"]#,
                    #'response_metadata': response["context"]
                }), 200
            except Exception as e:
                print(e)
                error_details = serialize_error_details(e)
                error_details_json = json.dumps(error_details, indent=4)
                print(error_details_json)
            return error_details_json, 400
        else:
            return jsonify({'error': 'Message is required'}), 400
    return jsonify({'error': 'Request must be JSON'}), 400

if __name__ == '__main__':    
    app.run(debug=True)
