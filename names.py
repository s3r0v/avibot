from telebot.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton

#### TOKEN ####
TOKEN = "2124576539:AAF99WADGA6vF1JJTA3YsVzDAkSpU0KXlUU"

#### BUTTONS ####

main_buttons = ["Профиль 💼", "Пополнение 💰", "Поддержка 🗣", "Парсинг 🔰"]
main_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
main_markup.row(main_buttons[0], main_buttons[1])
main_markup.row(main_buttons[2], main_buttons[3])

promo_markup = InlineKeyboardMarkup()
promo_markup.row(InlineKeyboardButton("Ввести промокод 📧", callback_data="promo"))

money_buttons = ["QIWI 🟠", "BTC BANKER 🏦"]
money_markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
money_markup.row(money_buttons[0], money_buttons[1])

check_markup = InlineKeyboardMarkup()
check_markup.add(InlineKeyboardButton(text = "Подтверждаю", callback_data="chkrules"))

#### TEXTS ####
welcome = "Добро пожаловать"
captcha_text = "Введите капчу" 
support = "Если есть вопросы по работе бота - пишите сюда @KOTSHOP_SUP"
instruction = "Загрузите, пожалуйста, таблицу"
choose_wallet = "Пожалуйста, выберите платёжную систему"
choose_quantity = "Пожалуйста, введите количество денег, которое вы хотите внести"
rules = ("Ознакомьтесь с правилами и нажмите кнопку подтверждения:\n\n"+
        "1. 📃 Общие правила\n"+
        "1.1 Возврат денежных средств осуществляется только на баланс бота.\n"+
        "1.2 Вывод денежных средств с баланса бота не осуществляется.\n"+
        "1.3 За неадекватное общение с поддержкой или администрацией может последовать отказ в обслуживании.\n"+
        "1.4 Администрация оставляет за собой право вносить любые изменения и дополнения в правила, без предупреждения.\n"+
        "1.5 В случае возникновения проблем с парсингом покупатель должен незамедлительно написать в поддержку.\n"+
        "1.6 Ответ администрации может занимать до 48 часов в среднем не дольше пары часов.\n"+
        "1.7 Администрация оставляет за собой право заблокировать любого пользователя, без возмещения средств на балансе.\n\n"+
        "Также подпишитесь на наши информационные ресурсы:\n\n@erascama")
# Текст профиля находится в коде бота
# Тексты со ссылками на платёжки также в коде бота


#### DATABASE ####
mysql_host = "188.225.58.59"
mysql_user = "root"
mysql_passwd = "pYTQ6MyL"
mysql_port = "3306"
mysql_database = "bot"
