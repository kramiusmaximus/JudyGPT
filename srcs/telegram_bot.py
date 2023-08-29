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
        self.application.run_webhook(listen="0.0.0.0", port=8443, cert='./certificate/YOURPUBLIC.pem', key='./certificate/YOURPRIVATE.key', webhook_url="https://109.93.43.89:8443/wh")
        logging.info("Telegram bot started.")

class TelegramChainBot(TelegramBot):
    def __init__(self, token, handlers, chain:myChain):
        super().__init__(token, handlers)
        self.chain = myChain

