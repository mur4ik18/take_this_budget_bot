import telebot
import os
from telebot import types
from databases import Database
import datetime
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS payments (
                                        id integer PRIMARY KEY,
                                        money float,
                                        name text NOT NULL,
                                        category text,
                                        date timestamp) """

db = Database()
db.create_table(sql_create_projects_table)
db.close()


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hi")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "help")


@bot.message_handler(commands=['payed'])
def payed(message):
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
        date = datetime.datetime.now()

        if call.data == "food":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "food",
                date
                ))
            print(p)
        elif call.data == "chimy":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "chimy",
                date
                ))
            print(p)
        elif call.data == "nyam":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "nyam",
                date
                ))
            print(p)

        elif call.data == "fun":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "fun",
                date
                ))
            print(p)

        elif call.data == "investing":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "investing",
                date
                ))
            print(p)
        elif call.data == "health":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "health",
                date
                ))
            print(p)
        elif call.data == "everyday":
            info = reponse_for_user(call).split(" ")
            p = db.write_payment((
                info[0],
                " ".join(info[1:]),
                "everyday",
                date
                ))
            print(p)

    db.close()


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
