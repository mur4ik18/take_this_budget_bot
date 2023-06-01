import telebot
import os
from telebot import types
from databases import Database
import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi")
    id = get_chat_id(message)

    db = Database()
    if not db.check_table(f"payments{id}"):
        sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS payments{id} (
                                                id integer PRIMARY KEY,
                                            money float,
                                            name text NOT NULL,
                                            category text,
                                            date timestamp) """
        db.create_table(sql_create_projects_table)
        db.close()
        bot.send_message(message.chat.id, "I was created for you database")
    else:
        bot.send_message(message.chat.id, "You have database")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "help")


@bot.message_handler(commands=['last_10'])
def last_10(message):
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"payments{id}"):
        bot.reply_to(message, "Use /start for create your own db")
    last = db.return_last_payments(id, 10)
    reponse = ""
    print(last)
    for i in last:
        reponse += f"{i[4].split(' ')[0]} - {i[3]} - {i[1]} - {i[2]}\n"
    bot.reply_to(message, reponse)


@bot.message_handler(commands=['payed'])
def payed(message):
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"payments{id}"):
        bot.reply_to(message, "Use /start for create your own db")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)

        item0 = types.InlineKeyboardButton("Еда", callback_data='food')
        item = types.InlineKeyboardButton("Химия", callback_data='chimy')
        item1 = types.InlineKeyboardButton("Хотелки", callback_data='nyam')
        item2 = types.InlineKeyboardButton("Развлечения", callback_data='fun')
        item3 = types.InlineKeyboardButton("Инвестиции", callback_data='investing')
        item4 = types.InlineKeyboardButton("Медицина", callback_data='health')
        item5 = types.InlineKeyboardButton("Повседневное",
                                           callback_data='everyday')
        markup.add(item0, item, item1, item2, item3, item4, item5)

        bot.reply_to(message, "За что ты заплатил(а)", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        db = Database()
        info = reponse_for_user(call).split(" ")
        p = db.write_payment(get_chat_id(call.message), (
            info[0],
            " ".join(info[1:]),
            call.data,
            datetime.datetime.now()
            ))
        print(p)


def reponse_for_user(call):
    bot.send_message(
            call.message.chat.id,
            "Сколько денег и на что именно ты потратил(а)?")
    a = get_message(call.message, "message")
    user_input_message = str(a).split("/")[-1]
    bot.send_message(call.message.chat.id,
                     f"Хорошо я добавл твою трату \
\n'{user_input_message}'")
    return user_input_message


def get_chat_id(message):
    id = int(message.chat.id)
    if id < 0:
        id = "_"+str(id*(-1))
    return id


def get_message(message, text):
    a = []

    def ret(message):
        a.clear()
        a.append(message.text)
        return False
    bot.register_next_step_handler(message, ret)
    while a == []:
        pass
    return a[0]


bot.infinity_polling()
