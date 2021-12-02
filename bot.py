import telebot
from names import *
import logging
import mysql.connector
import qiwi
from random import randint
from captcha.image import ImageCaptcha
import os
from pars import *
import math

bot = telebot.TeleBot(TOKEN)

choose_quantity_flag = False
captcha_flag = False
send_file_flag = False

# Подключение к БД
db = mysql.connector.connect(
    host=mysql_host,
    user=mysql_user,
    passwd=mysql_passwd,
    port=mysql_port,
    database=mysql_database,
    auth_plugin='mysql_native_password'
)

curs = db.cursor()



@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    global user_id
    if call.data == "check":
        curs.execute(f"SELECT deals FROM users WHERE user_id = {call.from_user.id}")
        result = qiwi.check_payment(call.from_user.id, curs.fetchall()[0][0], curs, db)
        if result:
            curs.execute(f"UPDATE users SET deals=deals+1 WHERE user_id={call.from_user.id};")
            db.commit()
            bot.send_message(call.from_user.id, "Платёж получен")
        else:
            bot.send_message(call.from_user.id, "Платёж не получен")
    elif call.data == "menu":
        bot.send_message(call.from_user.id, welcome, reply_markup=main_markup)
        

@bot.callback_query_handler(func=lambda call: call.data == "chkrules")
def chksub(message):
    bot.register_next_step_handler(message, check_promo(message))

def check_promo(message):
    if message.text in file_to_array("promocodes.txt"):
        curs.execute(f"UPDATE users SET money=money+20 WHERE user_id={message.from_user.id};")
        db.commit()
        bot.send_message(message.from_user.id, "Промокод успешно введён")
    else:
        bot.send_message(message.from_user.id, "Недействительный промокод")

@bot.callback_query_handler(func=lambda call: call.data == "chkrules")
def chksub(message):
    statuss = ['creator', 'administrator', 'member']
    user_status = str(bot.get_chat_member(chat_id="@infokotshop", user_id=message.from_user.id).status)
    user_status2 = str(bot.get_chat_member(chat_id="@erascama", user_id=message.from_user.id).status)
    if user_status in statuss and user_status2 in statuss:
        bot.send_message(message.from_user.id, welcome, reply_markup=main_markup)
    else:
        check_rules(message.from_user.id)



@bot.message_handler(commands=['start'])
def send_welcome(message):
    global referrer

    referrer = message.text[7:]
    user_id = message.from_user.id
    curs.execute(f"SELECT * FROM users WHERE user_id = '{user_id}';")
    if len(curs.fetchall()) == 0:
        bot.register_next_step_handler(message, register(message))
    else:
        bot.send_message(message.from_user.id, welcome, reply_markup=main_markup)

def register(message):
    global captcha_flag
    global text

    text = str(randint(10000,99999))
    image = ImageCaptcha(width = 280, height = 90)
    data = image.generate(text)
    name = f'{randint(1,1000)}.png'
    image.write(text, name)

    bot.send_photo(message.from_user.id, photo=open(name, 'rb'))
    os.remove(name)
    captcha_flag = True
    bot.register_next_step_handler(message, check_rules)

def check_rules(message):
    bot.send_message(message.from_user.id, rules, reply_markup=check_markup)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    if send_file_flag:
        curs.execute(f"SELECT money FROM users WHERE user_id={message.from_user.id}")
        balance = float(curs.fetchall()[0][0])
        if balance >= 840: 
            bot.send_message(message.from_user.id, "Ожидайте")
            bot.register_next_step_handler(message, parse_stage(message))
        else:
            bot.send_message(message.from_user.id, "Недостаточно средств на балансе (мин. 840 руб)")
    else:
        bot.send_message(message.from_user.id, "Команда не распознана")
    
def parse_stage(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    name_text = f"{message.from_user.id}.{randint(1,1000)}.xlsx"

    with open(name_text, 'wb') as name:
        name.write(downloaded_file)

    curs.execute(f"SELECT money FROM users WHERE user_id='{message.from_user.id}';")
    numbers = parse(handle_excel(name_text), name_text, math.ceil(curs.fetchall()[0][0]//12))

    curs.execute(f"UPDATE users SET money=money-{numbers*12} WHERE user_id={message.from_user.id};")
    db.commit()

    with open(name_text, 'rb') as name:
        bot.send_document(message.from_user.id, name)

    os.remove(name_text)

@bot.message_handler(content_types=['text']) 
def get_text_messages(message):
    global choose_quantity_flag
    global captcha_flag
    global referrer
    global send_file_flag

    if message.text == "Профиль 💼":
        user_id = message.from_user.id
        ref = f"https://t.me/daflksjdbot?start={user_id}"
        curs.execute(f"SELECT money FROM users WHERE user_id = {user_id}")
        bot.send_message(message.from_user.id, f"Реферальная ссылка - {ref}\nБаланс - {curs.fetchall()[0][0]}", reply_markup=promo_markup)

    elif message.text == "Пополнение 💰":
        bot.send_message(message.from_user.id, choose_quantity)
        choose_quantity_flag = True

    elif message.text == "Поддержка 🗣":
        bot.send_message(message.from_user.id, support, reply_markup=main_markup)
    
    elif message.text == "Парсинг 🔰":
        send_file_flag = True
        bot.send_message(message.from_user.id, instruction, reply_markup=main_markup)
    
    elif message.text == "QIWI 🟠":
        bot.send_message(message.from_user.id, choose_quantity)
    
    elif message.text == "BTC BANKER 🏦":
        bot.send_message(message.from_user.id, choose_quantity)

    else:
        if choose_quantity_flag:
            quantity = float(message.text)
            curs.execute(f"SELECT deals FROM users WHERE user_id = {message.from_user.id}")
            link = f"https://qiwi.com/payment/form/99?extra%5B%27account%27%5D=79023970023&amount={quantity}&amountFraction=0&extra%5B%27comment%27%5D={message.from_user.id}.{curs.fetchall()[0][0]}&currency=643"
            payment_markup = InlineKeyboardMarkup()
            payment_markup.add(InlineKeyboardButton(text = "Перейти к оплате", url = link))
            payment_markup.add(InlineKeyboardButton(text = "Проверить оплату", callback_data="check"))
            payment_markup.add(InlineKeyboardButton(text = "В главное меню", callback_data="menu"))
            bot.send_message(message.from_user.id, "Внесите средства\nВнимание! Не меняйте комментарий и валюту! В противном случае, платёж зачислен не будет", reply_markup=payment_markup)

        elif captcha_flag:
            if message.text == text:
                if referrer != '':
                        curs.execute(f"UPDATE users SET money=money+money*0.03 WHERE user_id={referrer};")
                        bot.send_message(referrer, "У вас новый реферал")
                        db.commit()
                curs.execute(f"INSERT INTO users (user_id) VALUES ({message.from_user.id});")
                db.commit()
                captcha_flag = False
                bot.send_message(message.from_user.id, welcome, reply_markup=main_markup)
            else:
                bot.send_message(message.from_user.id, "Ответ неверный")
                register(message.from_user.id, bot)
        else:
            bot.send_message(message.from_user.id, "Команда не распознана")
    



if __name__ == "__main__":
    #logger = telebot.logger   # Опции для дебага
    #telebot.logger.setLevel(logging.DEBUG)
    try:
        bot.polling()
    except Exception:
        bot.stop_polling()
        bot.polling()