from config import TOKEN, keys
from extensions import APIException, Converter
import telebot

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def reply1_message(message):
    text = "Привет! Я котик телеграмбота и сейчас расскажу, как пользоваться ботом. " \
           "Чтобы получить список доступных валют введи: /values\nА чтобы конвертировать валюту, введи " \
           "через пробел:\n<наименование валюты>  <наименование валюты в которую необходимо конвертировать>" \
           "  <необходимую сумму>"
    bot.reply_to(message, text)
    bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFO1RiyTcrmwLqng1uIUNywQkwaAv3xwAC0RkAAndEoEhpjM4FIR26xikE")


@bot.message_handler(commands=["values"])
def reply1_message(message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def reply1_message(message):
    try:
        values = message.text.split(" ")
        if len(values) != 3:
            raise APIException("Посмотрите внимательно, что-то не так ввели!")
        base, quote, amount = values
        if amount == "0":
            bot.send_sticker(message.chat.id, "CAACAgIAAxkBAAEFORFix_YzISttURo-w8cDCsO_lq2ipQACOxgAAucJ-EixC_lH4h3d8ikE")
            raise APIException("Ну и смысл тогда пользоваться конвертером? И так же ясно, что результат будет ноль!")
        total_amount = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f"Ошибка пользователя\n{e}")
    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        bot.send_message(message.chat.id, f"Итог:\n{amount} валюты {base.upper()} в валюту {quote.upper()} - {total_amount}")


bot.polling(none_stop=True)
