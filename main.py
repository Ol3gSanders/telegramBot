import telebot

TOKEN = '2075384018:AAEHOiQnUPkIrHTPTFqHX0w1THcazeLpPLc'

bot = telebot.TeleBot(TOKEN)

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('Начать')
salary, days, hour, per_hour, total, percent = 0, 0, 0, 0, 0, 0


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет, {0.first_name}!'.format(message.from_user))
    bot.send_message(message.chat.id, 'Данный бот выводит информацию о том, сколько ты заработал :)'
                                      '\nЧтобы это произошло, '
                                      'нажми на кнопку "Начать" внизу и следуй указаниям!', reply_markup=keyboard1)


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == 'Начать':
        bot.send_message(message.from_user.id, "Введи свой месячный оклад")
        bot.register_next_step_handler(message, get_salary)


def get_salary(message):
    global salary
    salary = int(message.text)
    bot.send_message(message.from_user.id, 'Введи количество рабочих дней в текущем месяце')
    bot.register_next_step_handler(message, get_days)


def get_days(message):
    global days
    days = int(message.text)
    bot.send_message(message.from_user.id, 'Если у тебя фиксированная ставка в час, самое время ее ввести.\n'
                                           'Если нет, введи 0')
    bot.register_next_step_handler(message, get_bid)



def get_bid(message):
    global per_hour
    per_hour = float(message.text)
    if per_hour == 0:
        per_hour = float(int(salary) / int(days)) / 8
    else:
        per_hour = float(message.text)
    bot.send_message(message.from_user.id, f'Твой оклад: {str(salary)} рублей\nКоличество рабочих дней: {str(days)}\n'
                                            f'Твоя ставка в час: {str(round(per_hour, 2))} рублей')
    bot.send_message(message.from_user.id, 'Сколько % ты отдаешь государству?')
    bot.register_next_step_handler(message, get_percent)


def get_percent(message):
    global percent
    percent = float(message.text)
    bot.send_message(message.from_user.id, 'Введи количество отработанных часов')
    if percent == 0:
        percent = 100
    else:
        percent = (100 - float(message.text))
    bot.register_next_step_handler(message, get_total)


def get_total(message):
    global hour
    global total
    global percent
    hour = float(message.text)
    total = float((hour * per_hour) * (percent / 100))
    if percent == 100:
        bot.send_message(message.from_user.id, f'Ты заработал {str(round(total, 2))} рублей')
    else:
        bot.send_message(message.from_user.id, f'Ты заработал {str(round(total, 2))} рублей после вычета НДФЛ')


bot.polling(none_stop=True, interval=0)

