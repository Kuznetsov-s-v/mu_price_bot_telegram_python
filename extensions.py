from config import keys, ExchangeRatesApi_key
import requests
import json

class APIException(Exception):
    pass

class API:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):

        if quote == base:
            raise APIException(f'Невозможно конвертировать одинаковые валюты {base}')
        try:
            quote_tiker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')
        try:
            base_tiker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')
        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={ExchangeRatesApi_key}'
                         # '&base=RUB'    # по умолчанию base=EUR, функция будет доступна только после перехода на платный тариф
                         '&symbols=USD,EUR,CNY,RUB')
        value = json.loads(r.content)  # получение всех словарей из r
        result = value['rates']  # присвоение словаря rates содержащего курсы валют
        base_r = result['RUB']  # base_r нужен для перевода всех валют в отношение к рублю, вместо базового евро.
        keys_two = {
            'USD': (1 / (base_r / result['USD'])),  # вычисление количества валюты за 1 рубль
            'EUR': (1 / base_r),
            'CNY': (1 / (base_r / result['CNY'])),
            'RUB': 1
        }
        return (keys_two[quote_tiker] / keys_two[base_tiker]) * amount # Возврат значения в totalbase
