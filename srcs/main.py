import os
import logging
import dotenv
from web_server import app

from telegram_bot_handlers import get_handlers
from telegram_bot import TelegramChainBot
from langchain_stuff import myChain

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()

def add_config(app, bot, port, debug):
    app.config['BOT'] = bot
    app.config['PORT'] = os.getenv('PORT', 443)
    app.config['HOST'] = '0.0.0.0'
    app.config['DEBUG'] = debug

if __name__ == "__main__":





    # print(f"Query: {res['query']}")
    # print(f"Query Topic: {res['query_topic']}")
    # print(f"Answer: {res['result']}")
    # print(f"Sources: {res['source_documents']}")
    chain = myChain()
    handlers = get_handlers(chain)
    bot = TelegramChainBot(os.getenv('TELEGRAM_BOT_TOKEN'), handlers, os.getenv('DOMAIN_NAME') + "herokuapp.com/wh", chain)
    add_config(app, bot, os.getenv('PORT', 433), os.getenv('DEBUG'))
    app.run(app.config['HOST'], app.config['PORT'], app.config['DEBUG'])




