import os
import logging
import dotenv
from requests import post
from telegram_bot import TelegramChainBot
from langchain_stuff import myChain
from fastapi import FastAPI, Response
from models import Update

dotenv.load_dotenv()
logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = FastAPI()
chain = myChain()
bot = TelegramChainBot(TELEGRAM_TOKEN, WEB_HOOK_URL, int(os.getenv('PORT')), chain)



@app.get('/test')
async def test_get():
    logger.info('/test request recieved')
    return 'test'

@app.post('/web_hook')
async def webhook(data: Update):
    logging.info(data)
    logging.info("web_hook request recieved")
    text = data.message.text
    response_text = bot.chain.handle_question(text)
    status_code = send_message(TELEGRAM_TOKEN, data.chat.id, response_text)

    return Response(status_code=status_code)

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    return post(url, payload)














