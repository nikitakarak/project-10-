import telebot
from telebot import types
token='2067543421:AAHKcOTfDy9fZBfw-jfFnGRfM0qgsOZsyyQ'
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
    elif message.text=="Вернуть предмет":
        bot.send_message(message.chat.id,'Введите номер предмета')
        bot.register_next_step_handler(message, return_object);        
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
    menu_button(message)

def get_object(message):
    idd = message.text
    user_id = message.from_user.id
    if cursor.execute("SELECT * FROM objects WHERE id=?", [idd]):
        bot.send_message(message.chat.id,'Предмет взят')
        cursor.execute("UPDATE objects SET user=(SELECT id FROM users WHERE user_id=?) WHERE id=?", [user_id,idd])
        conn.commit()
        menu_button(message)
        
        
def return_object(message):
    idd = message.text
    user_id = message.from_user.id
    if cursor.execute("SELECT * FROM objects WHERE id=?", [idd]):
        bot.send_message(message.chat.id,'Предмет возвращен')
        cursor.execute("UPDATE objects SET user=NULL WHERE id=?", [idd])
        conn.commit()
        menu_button(message)
        
        
def menu_button(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Взять предмет")
    item2=types.KeyboardButton("Вернуть предмет")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id,'Выберите что вам надо',reply_markup=markup)
    bot.register_next_step_handler(message, menu)
    
    
bot.infinity_polling( interval=1)
