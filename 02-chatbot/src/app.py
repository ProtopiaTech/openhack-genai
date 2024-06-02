import json
from flask import Flask, render_template, request, jsonify

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
                return jsonify({
                    'content': message,
                    'response_metadata': "tu będą metadane"
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
