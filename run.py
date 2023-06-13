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
    # if user have not a database with payments we will create
    if not db.check_table(f"payments{id}"):
        sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS
                                            payments{id} (
                                            id integer PRIMARY KEY,
                                            money float,
                                            name text NOT NULL,
                                            category text,
                                            date timestamp) """
        db.create_table(sql_create_projects_table)
        bot.send_message(message.chat.id, "I was created for you database")
    # if user have not a database with categories we will create
    if not db.check_table(f"categories{id}"):
        sql_create_projects_table = f""" CREATE TABLE IF NOT EXISTS
                                            categories{id} (
                                            id integer PRIMARY KEY,
                                            category text) """
        db.create_table(sql_create_projects_table)
        bot.send_message(message.chat.id, "I was created for you database")

    db.close()
    bot.send_message(message.chat.id, "Now you can add yours categories\n\
            you can use a command /add_categories")


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "help")


@bot.message_handler(commands=['last_10'])
def give_last_10(message):
    """
        This function give a list with last 10 payments
        what you are added
    """
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


@bot.message_handler(commands=['add_categories'])
def add_categories(message):
    """
        This function add new category in this chat table
    """
    bot.send_message(message.chat.id, "You can write category name")
    user_message = get_message(message, "message")
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"categories{id}"):
        bot.reply_ty(user_message, "Use /start for create your own db")
        return
    if db.write_new_category(id, user_message):
        bot.send_message(message.chat.id, "We are added new category")
    else:
        bot.send_message(message.chat.id, "Category with this name exist!\n\
You can use /categories for show the list of the categories")


@bot.message_handler(commands=['categories'])
def categories(message):
    """
        Show list of categories
    """
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"payments{id}") or not db.check_table(f"categories{id}"):
        bot.reply_to(message, "Use /start for create your own db")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        categories = db.get_categories(id)
        for i in categories:
            item = types.InlineKeyboardButton(i[-1], callback_data='categories')
            markup.add(item)

        bot.reply_to(message, "Your categories:", reply_markup=markup)


@bot.message_handler(commands=['delete_category'])
def delete_categories(message):
    """
        delete category
        Here user can click on button for choise
    """
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"payments{id}") or not db.check_table(f"categories{id}"):
        bot.reply_to(message, "Use /start for create your own db")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        categories = db.get_categories(id)
        for i in categories:
            item = types.InlineKeyboardButton(i[-1], callback_data=f'delete_{i[-1]}')
            markup.add(item)

        bot.reply_to(message, "Your categories:", reply_markup=markup)


@bot.message_handler(commands=['payed'])
def payed(message):
    db = Database()
    id = get_chat_id(message)
    if not db.check_table(f"payments{id}") or not db.check_table(f"categories{id}"):
        bot.reply_to(message, "Use /start for create your own db")
    else:
        markup = types.InlineKeyboardMarkup(row_width=2)
        categories = db.get_categories(id)
        for i in categories:
            item = types.InlineKeyboardButton(i[-1], callback_data=i[-1])
            markup.add(item)

        bot.reply_to(message, "Choise category please", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    if call.message:
        # after "/categories" we shuldnt verifier
        if call.data == "categories":
            print(call.data[:5])
        # if we want delete categories
        elif call.data[:6] == "delete":
            category = call.data[7:]
            print(category)
            db = Database()
            id = get_chat_id(call.message)
            db.delete_categories(id, category)
            bot.send_message(call.message.chat.id, f"I was deleted  your category with name - {category}")
        # if we add new payment
        else:
            db = Database()
            bot.send_message(
                    call.message.chat.id,
                    "Сколько денег и на что именно ты потратил(а)?")
            a = get_message(call.message, "message")
            user_input_message = str(a).split("/")[-1]
            bot.send_message(call.message.chat.id,
                             f"Хорошо я добавл твою трату \
        \n'{user_input_message}'")
            info = user_input_message.split(" ")
            p = db.write_payment(get_chat_id(call.message), (
                info[0],
                " ".join(info[1:]),
                call.data,
                datetime.datetime.now()
                ))
            print(p)


def get_chat_id(message):
    id = int(message.chat.id)
    if id < 0:
        id = "_"+str(id*(-1))
    return id


def get_message(message, text):
    """
        get a message what an user will write
    """
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
