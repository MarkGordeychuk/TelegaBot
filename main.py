import telebot

from config import TOKEN
from currencies import values
from extensions import ConverterException, Converter


def main():
    bot = telebot.TeleBot(TOKEN)

    @bot.message_handler(commands=["start", "help"])
    def command_help(message: telebot.types.Message):
        bot.reply_to(message, "Привет. Я бот-конвертер валют.\n" +
                              "Для конвертации валюты введите:\n" +
                              "<имя_начальной_валюты> <имя_конечной_валюты> <количество>\n" +
                              "Для просмотра списка возможных вальт введите: /values\n" +
                              "Введите /help, если хотите ещё раз увидеть это сообщение")

    @bot.message_handler(commands=["values"])
    def command_values(message: telebot.types.Message):
        bot.reply_to(message, "\n".join(("Список возможных валют:", *[f"{a} ({b})" for a, b in values.items()])))

    @bot.message_handler()
    def convert(message: telebot.types.Message):
        try:
            conv = Converter.from_text(message.text)
            bot.reply_to(message, f"{conv.amount} {conv.val_from} = {conv.convert()} {conv.val_to}")
        except ConverterException as e:
            bot.reply_to(message, f"Ошибка ввода: {e}")
        except Exception as e:
            bot.reply_to(message, f"Ошибка: {e}")

    bot.polling()


if __name__ == '__main__':
    main()
