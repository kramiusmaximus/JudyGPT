import os

import requests
from flask import Flask, request

from srcs.langchain_stuff import myChain
from srcs.telegram_bot_handlers import get_handlers
from telegram_bot import TelegramChainBot


app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return 'test'

@app.route('/web_hook', methods=['POST'])
def webhook():
    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    response_text = f"You said: {text}"
    send_message(chat_id, response_text)
    return 'ok'

def send_message(chat_id, text):
    token = 'YOUR_TELEGRAM_BOT_TOKEN'
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()



