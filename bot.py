from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    chat_id = data['chat_id']
    message = data['message']
    
    response = requests.post(TELEGRAM_API_URL, json={
        'chat_id': chat_id,
        'text': message
    })
    
    return jsonify(response.json())

if __name__ == '__main__':
    app.run(port=5000)
