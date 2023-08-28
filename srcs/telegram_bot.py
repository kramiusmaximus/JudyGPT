import logging
from telegram.ext import filters, ApplicationBuilder
from langchain_stuff import myChain


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

chat_history = {}

class TelegramBot:
    def __init__(self, token, handlers):
        self.application = ApplicationBuilder().token(token).build()
        self.application.add_handlers(handlers)
        logging.debug("Telegram bot initialized")
    def run(self):
        self.application.run_polling()
        logging.info("Telegram bot started.")

class TelegramChainBot(TelegramBot):
    def __init__(self, token, handlers, chain:myChain):
        super().__init__(token, handlers)
        self.chain = myChain

