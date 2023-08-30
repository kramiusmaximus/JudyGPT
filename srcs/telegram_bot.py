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

class TelegramChainBot:
    def __init__(self, token, handlers, url, port, chain:myChain):
        self.application = ApplicationBuilder().token(token).build()
        self.application.add_handlers(handlers)
        self.web_hook_url = url
        self.port = port
        self.chain = chain

        logging.debug("Telegram bot initialized")

    def run(self):
        self.application.run_webhook(listen="0.0.0.0", port=self.port, webhook_url=self.web_hook_url)


