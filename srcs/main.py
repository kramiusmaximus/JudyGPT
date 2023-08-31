import os
import logging
import dotenv

from telegram_bot import TelegramChainBot
from langchain_stuff import myChain

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

WEB_HOOK_PATH = '/web_hook'
WEB_HOOK_URL = os.getenv('DOMAIN_NAME', 'http://192.168.1.90') + WEB_HOOK_PATH

def add_config(app, bot, port, debug):
    app.config['BOT'] = bot
    app.config['PORT'] = port
    app.config['HOST'] = '0.0.0.0'
    app.config['DEBUG'] = debug



if __name__ == "__main__":
    # print(f"Query: {res['query']}")
    # print(f"Query Topic: {res['query_topic']}")
    # print(f"Answer: {res['result']}")
    # print(f"Sources: {res['source_documents']}")
    chain = myChain()
    #bot = TelegramChainBot(os.getenv('TELEGRAM_BOT_TOKEN'), WEB_HOOK_URL, os.getenv('PORT'), chain)

    from web_server import app
    add_config(app, None, os.getenv('PORT', 443), os.getenv('DEBUG'))
    app.run(app.config['HOST'], app.config['PORT'], app.config['DEBUG'])
    logging.info("Flask app started")




