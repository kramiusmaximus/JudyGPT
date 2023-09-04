import os
import logging
import dotenv
from requests import post
from telegram_bot import TelegramChainBot
from langchain_stuff import myChain
from fastapi import FastAPI, Response
from models import Update
from logging_setup import setup

dotenv.load_dotenv()

setup()
logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH

app = FastAPI()

chain = myChain()
bot = TelegramChainBot(os.getenv('TELEGRAM_BOT_TOKEN'), WEB_HOOK_URL, int(os.getenv('PORT')), chain)

@app.get('/test')
async def test_get():
    logger.error('/test request recieved')
    return 'test'

@app.post('/web_hook')
def webhook(data: Update):
    logging.info(data)
    logging.info("web_hook request recieved")
    text = data.message.text
    status_code = bot.chain.handle_question(text)

    return Response(status_code=status_code)

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    return post(url, payload)








