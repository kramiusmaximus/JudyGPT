import os
import logging
import dotenv
from web_server import app

from telegram_bot_handlers import get_handlers
from telegram_bot import TelegramChainBot
from langchain_stuff import myChain

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME') + WEB_HOOK_PATH

if __name__ == "__main__":





    # print(f"Query: {res['query']}")
    # print(f"Query Topic: {res['query_topic']}")
    # print(f"Answer: {res['result']}")
    # print(f"Sources: {res['source_documents']}")
    chain = myChain()
    handlers = get_handlers(chain)
    bot = TelegramChainBot(os.getenv('TELEGRAM_BOT_TOKEN'), handlers, WEB_HOOK_URL, chain)
    app.run(app.config['HOST'], app.config['PORT'], app.config['DEBUG'])




