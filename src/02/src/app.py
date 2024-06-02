import json
from flask import Flask, render_template, request, jsonify
import os
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI



def serialize_error_details(e):
    error_details = {}
    for key, value in e.__dict__.items():
        try:
            json.dumps(value)  # Test if the value is JSON serializable
            error_details[key] = value
        except TypeError:
            error_details[key] = str(value)  # Convert non-serializable values to strings
    return error_details

app = Flask(__name__)

with app.app_context():
   load_dotenv()
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    if request.is_json:
        data = request.get_json()
        print(data)
        message = data.get('message', '')
        print(message)
        if message:
            try:
                response = llm.invoke(message)
                return jsonify({
                    'content': response.content,
                    'response_metadata': response.response_metadata
                }), 200
            except Exception as e:
                print(e)
                error_details = serialize_error_details(e)
                error_details_json = json.dumps(error_details)
                print(error_details_json)
            return error_details_json, 400
        else:
            return jsonify({'error': 'Message is required'}), 400
    return jsonify({'error': 'Request must be JSON'}), 400


if __name__ == '__main__':    
    app.run()
