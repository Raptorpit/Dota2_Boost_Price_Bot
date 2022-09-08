import telebot
from telebot import types

import config
import parcing
import record
import calculate

token = config.token
bot = telebot.TeleBot(token)

# Парсим html данные аккаунтов
acc = parcing.parsing()
# Записываем нужные данные в список
acc_list = record.record_html(acc)
# Пишем данные из списка в csv файл
record.record_in_file(acc_list)
# Считаем из файла средние значения и записываем их в словарь в формате "среднее значение:[список диапазона ммр]"
avg_price_dict = calculate.average_price()
# Считаем стоимость буста
# boost_sum = calculate.boost_price(avg_price_dict,starting_mmr,ending_mmr)

# Таблица средних цен
grp_data = calculate.grp_data()
# Храню start_mmr из сообщения пользователя
start_mmr_list = []
# Хранится список чисел в формате str
mmr_range = []
for i in range(0, 8501):
    mmr_range.append(str(i))


@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_mmr = types.KeyboardButton("Узнать цену буста")
    button_mmr_table = types.KeyboardButton("Таблица средних цен за буст")
    markup.add(button_mmr, button_mmr_table)
    msg = bot.send_message(message.chat.id, text="Привет!Я подскажу среднюю стоимость буста аккаунта.",
                           reply_markup=markup)
    bot.register_next_step_handler(msg, start_mmr_say)


def start_mmr_say(message):
    if message.text == "Узнать цену буста":
        msg = bot.send_message(message.chat.id, text=f"Введи начальный ммр аккаунта:\n"
                                                     f"(Для более точного расчета вводи ммр кратный 100)")
        bot.register_next_step_handler(msg, end_mmr_say)
    if message.text == "Таблица средних цен за буст":
        bot.send_message(message.chat.id, text=grp_data)


def end_mmr_say(message):
    start_mmr = message.text
    if message.text in mmr_range:
        start_mmr_list.append(start_mmr)
        msg = bot.send_message(message.chat.id, text=f"Введи конечный ммр аккаунта:\n"
                                                     f"(Для более точного расчета вводи ммр кратный 100)")
        bot.register_next_step_handler(msg, say_boost_price)
    if message.text == "Таблица средних цен за буст":
        bot.send_message(message.chat.id, text=grp_data)
    else:
        msg = bot.send_message(message.chat.id, text="Введи пожалуйста число в диапазоне от 0 до 8500")
        bot.register_next_step_handler(msg, end_mmr_say)


def say_boost_price(message):
    end_mmr = message.text
    if end_mmr in mmr_range:
        start_mmr = int(start_mmr_list[0])
        end_mmr = int(end_mmr)
        bot.send_message(message.chat.id,
                         text=f"≈{(calculate.boost_price(avg_price_dict, start_mmr, end_mmr)):.2f} ₽ \n"
                              f"Сумма рассчитана на основе средней цены предложений бустеров с сайта Funpay")
        start_mmr_list.pop(0)
    if message.text == "Таблица средних цен за буст":
        bot.send_message(message.chat.id, text=grp_data)
    else:
        msg = bot.send_message(message.chat.id, text="Введи пожалуйста число в диапазоне от 0 до 8500")
        bot.register_next_step_handler(msg, say_boost_price)


@bot.message_handler(content_types=['text'])
def start_mmr_say(message):
    if message.text == "Узнать цену буста":
        msg = bot.send_message(message.chat.id, text=f"Введи начальный ммр аккаунта:\n"
                                                     f"(Для более точного расчета вводи ммр кратный 100)")
        bot.register_next_step_handler(msg, end_mmr_say)
    if message.text == "Таблица средних цен за буст":
        bot.send_message(message.chat.id, text=grp_data)


bot.infinity_polling()
