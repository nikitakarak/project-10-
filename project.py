import telegram
from telegram.ext import Updater
import logging
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

TOKEN = '2067543421:AAHKcOTfDy9fZBfw-jfFnGRfM0qgsOZsyyQ'
bot = telegram.Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
dispatcher.add_handler(MessageHandler(Filters.all))


def on_message(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text="Напишите свои имя, фамилию и класс")


def start(update, context):
    keyboard = [[InlineKeyboardButton("Оставить заявку")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Нажмите кнопку, чтобы оставить заявку на оборудование', reply_markup=reply_markup)
    dispatcher.add_handler(MessageHandler(Filters.all, on_message))


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updates = bot.get_updates()
print([upd.message.text for upd in updates])

chat_id = bot.get_updates()[-1].message.chat_id
bot.send_message(chat_id=chat_id, text="")

UPDATE_ID = None
for update in bot.get_updates(offset=UPDATE_ID, timeout=10):
    update.message.reply_text("")

updater.start_polling()
