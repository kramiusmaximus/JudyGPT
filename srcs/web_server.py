import logging
import os

import requests
from flask import Flask, request

from langchain_stuff import myChain
from telegram_bot import TelegramChainBot

INTRODUCTION_TEMPLATE = "Добрый день! я бот Юрист. Задайте ваш юридический вопрос, и опишите его максимально подробно. Я посотраюсь на ваш вопрос ответить."


app = Flask(__name__)

@app.route('/', methods=['GET'])
def test():
    return 'test'

@app.route('/web_hook', methods=['POST'])
def webhook():
    logging.info("web_hook request recieved")
    bot: TelegramChainBot = app.config['BOT']

    data = request.json
    chat_id = data['message']['chat']['id']
    text = data['message']['text']
    response_text = bot.chain.handle_question(text)
    send_message(bot.token, chat_id, response_text)
    return 'ok'

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}
    response = requests.post(url, json=payload)
    return response.json()



