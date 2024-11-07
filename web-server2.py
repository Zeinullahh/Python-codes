from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo'
CHAT_ID = '987654321'  # Replace with your actual chat ID

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    message = data.get('message')
    if message:
        chat_id = message['chat']['id']
        text = message['text']
        send_message(chat_id, text)
    return '', 200

@app.route('/send_message', methods=['POST'])
def send_message_to_telegram():
    data = request.get_json()
    text = data.get('text')
    send_message(CHAT_ID, text)
    return jsonify({'status': 'success'}), 200

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
