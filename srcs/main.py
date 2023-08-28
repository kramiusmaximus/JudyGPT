import os
import logging
import dotenv
from telegram_bot_handlers import get_handlers
from telegram_bot import TelegramChainBot
from langchain_stuff import myChain

logging.basicConfig(level=logging.INFO)
dotenv.load_dotenv()



if __name__ == "__main__":





    # print(f"Query: {res['query']}")
    # print(f"Query Topic: {res['query_topic']}")
    # print(f"Answer: {res['result']}")
    # print(f"Sources: {res['source_documents']}")

    chain = myChain()
    handlers = get_handlers(chain)
    bot = TelegramChainBot(os.getenv('TELEGRAM_BOT_TOKEN'), handlers, chain)
    bot.run()




