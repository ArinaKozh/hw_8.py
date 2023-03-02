
import sqlite3
import telebot
from random import *
import json
from telebot import types
nums=[]

try:
    sqlite_connection = sqlite3.connect('sqlite_python.db', check_same_thread=False)
    sqlite_create_table_query = '''CREATE TABLE IF NOT EXISTS list (
                                name TEXT NOT NULL,
                                number text NOT NULL);'''

    cursor = sqlite_connection.cursor()
    print("База данных подключена к SQLite")
    cursor.execute(sqlite_create_table_query)
    sqlite_connection.commit()
    print("Таблица SQLite создана")


except sqlite3.Error as error:
    print("Ошибка при подключении к sqlite", error)
"""
finally:
    if (sqlite_connection):
        sqlite_connection.close()
        print("Соединение с SQLite закрыто")

"""

bot = telebot.TeleBot('6274590520:AAGbUn24Tn5-3GWwpSrl841egFKM4xlp1e8')

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id,"Бот начал работу, чтобы увидеть список команд, введите команду /help")

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id,"Бот выполняет команды:\n"
                     "/start - начать работу\n"
                     "/stop - завершить работу\n"
                     "/all - показать все номера\n"
                     "Чтобы добавить новый номер, просто введите имя и номер через пробел")

def add_user(message,name,num):
    bot.send_message(message.chat.id,"Добавлен новый номер")
    cursor.execute('INSERT INTO list (name, number) VALUES(?, ?)', (name, num))
    sqlite_connection.commit()

@bot.message_handler(commands=['all'])
def show_all(message):
    cursor.execute("SELECT * FROM list;")
    fetch = cursor.fetchall()
    bot.send_message(message.chat.id,"Вот все номера:")
    bot.send_message(message.chat.id, ','.join([f'{i[0]}:{i[1]}' for i in fetch]))

@bot.message_handler(commands=['stop'])
def start_message(message):
     bot.send_message(message.chat.id,"До свидания")
     bot.stop_polling()
     


@bot.message_handler(content_types='text')
def input(message):
    try:
        txt = message.text.split()
        s = tuple(txt)
        cursor.execute("SELECT * FROM list;")
        fetch = cursor.fetchall()
        if s not in fetch:
            add_user(message,txt[0],txt[1])
        else:
            bot.send_message(message.chat.id,"Такой номер уже записан")

    except:
        bot.send_message(message.chat.id,"Неверно ввели данные")



bot.polling()

