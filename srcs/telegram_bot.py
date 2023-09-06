import logging
import os

import requests
from telegram.ext import filters, ApplicationBuilder
from langchain_stuff import Core


logger = logging.getLogger('prom') if os.getenv('ENV') == 'prom' else logging.getLogger('dev')


chat_history = {}

class TelegramChainBot:
    def __init__(self, token, url, port, chain:Core):
        self.token = token
        self.application = ApplicationBuilder().token(token).build()
        self.web_hook_url = url
        self.port = port
        self.chain: Core = chain
        #self.application.run_webhook(port=self.port, webhook_url=self.web_hook_url)



