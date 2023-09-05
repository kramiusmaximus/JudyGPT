import os
import logging
import dotenv
from requests import post
from starlette.requests import Request

from telegram_bot import TelegramChainBot
from langchain_stuff import myChain
from fastapi import FastAPI, Response, APIRouter, Depends
from models import Message

dotenv.load_dotenv()
logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = FastAPI()
api_router = APIRouter()
chain = myChain()
bot = TelegramChainBot(TELEGRAM_TOKEN, WEB_HOOK_URL, int(os.getenv('PORT')), chain)

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
async def webhook(data: Message):
    logging.info(data)
    logging.info("web_hook request recieved")
    text = data.text
    response_text = bot.chain.handle_question(text)
    response = send_message(TELEGRAM_TOKEN, data.chat.id, response_text)

    return Response(status_code=response.status_code)

app.include_router(api_router, dependencies=[Depends(log_request_info)])

def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    return post(url, payload)














