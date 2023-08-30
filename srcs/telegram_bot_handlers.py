from telegram import Update
from telegram.ext import ContextTypes, ContextTypes, CommandHandler, MessageHandler, filters
from langchain_stuff import myChain

INTRODUCTION_TEMPLATE = "Добрый день! я бот Юрист. Задайте ваш юридический вопрос, и опишите его максимально подробно. Я посотраюсь на ваш вопрос ответить."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INTRODUCTION_TEMPLATE)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.username
    user_msg = update.message.text


    await context.bot.send_message(chat_id=update.effective_chat.id, text=user_msg) # todo: remove ting


def get_handlers(chain:myChain):
    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), chain.handle_message)
    return [start_handler, message_handler]