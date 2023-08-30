import logging

import requests
from flask import Flask, request
from telegram.ext import filters, ApplicationBuilder
from langchain_stuff import myChain


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

chat_history = {}

class TelegramBot:

    def __init__(self, token, handlers, url):
        self.application = ApplicationBuilder().token(token).build()
        self.application.add_handlers(handlers)
        self.web_hook_url = url

        logging.debug("Telegram bot initialized")

    def run(self):
        self.application.run_webhook(listen="0.0.0.0", port=443, webhook_url=self.web_hook_url)

        logging.info("Telegram bot started.")


class TelegramChainBot(TelegramBot):
    def __init__(self, token, handlers, url, chain:myChain):
        super().__init__(token, handlers, url)
        self.chain = chain

