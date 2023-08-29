import os

import requests
from flask import Flask, request
import dotenv

dotenv.load_dotenv()

app = Flask(__name__)

@app.route('/wh', methods=['POST'])
def webhook():
    data = request.json
    # process the incoming message data here
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    # handle the message and craft a response
    response_text = f"You said: {text}"
    send_message(chat_id, response_text)
    return 'ok'

def send_message(chat_id, text):
    # send a message to the specified chat ID
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()

if __name__ == '__main__':
    # run the app with SSL context for secure webhook communication
    app.run(host='0.0.0.0', port=os.getenv('PORT'), ssl_context='adhoc')

