import os
import logging
import traceback
from asyncio import Future, Task
from time import sleep

import dotenv
from requests import post
from starlette.requests import Request
from fastapi import FastAPI, Response, APIRouter, Depends
from models import Update
from langchain_stuff import Core
import asyncio

dotenv.load_dotenv()
logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH
TELEGRAM_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

app = FastAPI()
api_router = APIRouter()
chain = Core(os.getenv('PINECONE_API_KEY'), os.getenv('PINECONE_ENVIRONMENT'), os.getenv('PINECONE_INDEX_NAME'), search_k=5, model_name='gpt-4')
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
    task = loop.create_task(handle_webhook_message(TELEGRAM_TOKEN, message.chat.id, message.text))
    task.add_done_callback(callback)

    return Response(status_code=200)

app.include_router(api_router, dependencies=[Depends(log_request_info)])


async def handle_webhook_message(token, chat_id, message_text):
    response_text = chain.handle_question(message_text)
    send_message(token, chat_id, response_text)
    logging.info('webhook message handled')


def send_message(token, chat_id, text):
    url = f'https://api.telegram.org/bot{token}/sendMessage'
    payload = {'chat_id': chat_id, 'text': text}

    return post(url, payload)


def callback(task:Task):
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.

    except Exception:  # pylint: disable=broad-except
        logger.exception('Exception raised by task = %r', task)
