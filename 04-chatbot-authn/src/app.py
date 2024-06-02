import json
from flask import Flask, render_template, request, jsonify
import os
from helpers.authorization import requires_jwt_authorization, AuthError

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
  
@app.errorhandler(AuthError)
def handle_auth_error(ex):
    response = jsonify(ex.error)
    response.status_code = ex.status_code
    return response

@app.route('/')
def index():
    client_id = os.getenv('CLIENT_ID')
    tenant_id = os.getenv('TENANT_ID')
    return render_template('index.html', client_id=client_id, tenant_id=tenant_id)

@app.route('/chat', methods=['POST'])
@requires_jwt_authorization()
def chat():
    if request.is_json:
        data = request.get_json()
        print(data)
        message = data.get('message', '')
        print(message)
        if message:
            try:
                return jsonify({
                    'content': message,
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
    app.run()
