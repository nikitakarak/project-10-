import telebot
from telebot import types
token='5255737415:AAFMEbBle3SfOCuyzMp9jV_VCnZTP6C2pK0'
bot=telebot.TeleBot(token)
import sqlite3
conn = sqlite3.connect('db11.db', check_same_thread=False)
cursor = conn.cursor()


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id,'Привет, введите ФИО')
    user_id = message.from_user.id
    cursor.execute("REPLACE INTO users (user_id) VALUES (?)", [user_id])
    conn.commit()
    bot.register_next_step_handler(message, get_fio)
    
    
    

@bot.message_handler(content_types='text')
def menu(message):
    if message.text=="Взять предмет":
        bot.send_message(message.chat.id,'Введите номер предмета')
        bot.register_next_step_handler(message, get_object);
    else :
        bot.send_message(message.chat.id,'Неизвестная команда')
        bot.register_next_step_handler(message, menu);
        
def get_fio(message): 
    fio = message.text;
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET fio = ? WHERE user_id = ?", [fio,user_id])
    conn.commit()
    bot.send_message(message.from_user.id, 'Введите класс');
    bot.register_next_step_handler(message, get_class);
    
    
def get_class(message): 
    classs = message.text;
    user_id = message.from_user.id
    cursor.execute("UPDATE users SET class = ? WHERE user_id = ?", [classs,user_id])
    conn.commit()
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Взять предмет")
    markup.add(item1)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    bot.register_next_step_handler(message, menu);

def get_object(message):
    idd = message.text
    if cursor.execute("SELECT * FROM objects WHERE id=?", [idd]):
        bot.send_message(message.chat.id,'Предмет взят на 2 недели')
    
    
bot.infinity_polling( interval=10)