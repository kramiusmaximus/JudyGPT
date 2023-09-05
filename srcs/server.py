import os
import logging
import dotenv
from requests import post
from starlette.requests import Request

from telegram_bot import TelegramChainBot
from langchain_stuff import myChain
from fastapi import FastAPI, Response, APIRouter, Depends
from models import Update
import asyncio

dotenv.load_dotenv()
logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = FastAPI()
api_router = APIRouter()
chain = myChain()
bot = TelegramChainBot(TELEGRAM_TOKEN, WEB_HOOK_URL, int(os.getenv('PORT')), chain)
loop = asyncio.get_event_loop()

async def log_request_info(request: Request):
    request_body = await request.json()

    logger.info(
        f"{request.method} request to {request.url} metadata\n"
        f"\tHeaders: {request.headers}\n"
        f"\tBody: {request_body}\n"
        f"\tPath Params: {request.path_params}\n"
        f"\tQuery Params: {request.query_params}\n"
        f"\tCookies: {request.cookies}\n"
    )

@api_router.get('/test')
async def test_get():
    logger.info('/test request recieved')
    return 'test'

@api_router.post('/web_hook')
async def webhook(update: Update):
    message = update.message
    logging.info(message)
    logging.info("web_hook request recieved")
    loop.run_in_executor(None, handle_webhook_message, TELEGRAM_TOKEN, message.chat.id, message.text)

    return Response(status_code=200)

app.include_router(api_router, dependencies=[Depends(log_request_info)])

def handle_webhook_message(token, chat_id, message_text):
    response_text = bot.chain.handle_question(message_text)
    send_message(token, chat_id, response_text)
    logging.info('webhook message handled')

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    return post(url, payload)

