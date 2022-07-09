import requests
import json
from config import keys


class APIException(Exception):
    pass


class Converter():
    @staticmethod
    def get_price(base, quote, amount):
        if base == quote:
            raise APIException(f"Нельзя переводить одну валюту в себя же - {base}!")

        try:
            quote_tick = keys[quote]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {quote}")

        try:
            base_tick = keys[base]
        except KeyError:
            raise APIException(f"Не удалось обработать валюту {base}")

        try:
            amount = float(amount)
        except ValueError:
            raise APIException(f"Не удалось обработать количество - {amount}")

        response = requests.get("https://cdn.cur.su/api/latest.json")
        rates = json.loads(response.content)['rates']
        total_amount = round(rates[quote_tick] / rates[base_tick] * amount, 3)
        return total_amount
