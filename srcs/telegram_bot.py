import logging

import requests
from flask import Flask, request
from telegram.ext import filters, ApplicationBuilder
from langchain_stuff import myChain


logging.basicConfig(
    level=logging.INFO
)

chat_history = {}

class TelegramChainBot:
    def __init__(self, token, url, port, chain:myChain):
        self.token = token
        self.application = ApplicationBuilder().token(token).build()
        self.web_hook_url = url
        self.port = port
        self.chain: myChain = chain
        logging.info(f"port:{self.port}, url: {self.web_hook_url}")
        self.application.run_webhook(port=self.port, webhook_url=self.web_hook_url)



