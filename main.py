import telebot
from config import TOKEN, keys
bot = telebot.TeleBot(TOKEN)

class ConvertionException(Exception):
    pass

class APIException:
    @staticmethod
    def convert(quote: str, base: str, amount: str):
        if quote == base:
            raise ConvertionException(f'Невозможно конвертировать одинаковые валюты {base}')
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {quote}')
        try:
            base_tiker = keys[base]
        except KeyError:
            raise ConvertionException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise ConvertionException(f'Не удалось обработать количество {amount}')
        return (quote_tiker / base_tiker) * amount

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Привет, это вводная инструкция'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):

    values = message.text.split(' ')
    if len(values) != 3:
        raise ConvertionException('Количество параметров неверно')
    quote, base, amount = values
    total_base = APIException.convert(quote , base, amount)
    text = f'цена {amount} {base} в {quote} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling()