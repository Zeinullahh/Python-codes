from flask import Flask, request
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = '7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo'
CHAT_ID = 1  # You can set this dynamically based on your needs

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    message = update.get('message')
    if message:
        chat_id = message['chat']['id']
        text = message['text']

        # Here you can process the incoming message and decide how to respond
        response_text = f"Received your message: {text}"  # Replace with your response logic
        send_message(chat_id, response_text)

    return '', 200

def send_message(chat_id, text):
    url = f'https://api.telegram.org/bot7637744571:AAH5dNLsd-kXReU7MSfEiy5W3nrqFecMazo/sendMessage'
    requests.post(url, json={'chat_id': chat_id, 'text': text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

