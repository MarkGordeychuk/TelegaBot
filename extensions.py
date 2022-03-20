import requests
import json

from config import API_KEY
from currencies import values


class ConverterException(Exception):
    pass


class Converter:
    def __init__(self, val_from: str, val_to: str, amount: float):
        if val_to == val_from:
            raise ConverterException("Нет нужды конвертировать валюту саму в себя. 😀")

        self._val_from = val_from
        self._val_to = val_to
        self._amount = amount

    @property
    def val_from(self):
        return self._val_from

    @property
    def val_to(self):
        return self._val_to

    @property
    def amount(self):
        return self._amount

    @staticmethod
    def from_text(text: str):
        splitted_text = text.lower().split()

        if len(splitted_text) != 3:
            raise ConverterException("Неправильное количество аргументов")

        try:
            val_from = values[splitted_text[0]]
        except KeyError:
            raise ConverterException("Неверная валюта: " + splitted_text[0])

        try:
            val_to = values[splitted_text[1]]
        except KeyError:
            raise ConverterException("Неверная валюта: " + splitted_text[1])

        try:
            amount = float(splitted_text[2])
        except ValueError:
            raise ConverterException("Введено некорректное число")

        return Converter(val_from, val_to, amount)

    def convert(self):
        # Так не работает :(
        # r = requests.get("http://api.exchangeratesapi.io/v1/convert" +
        #                  f"?access_key={API_KEY}" +
        #                  f"&from={self.val_from}" +
        #                  f"&to={self.val_to})" +
        #                  f"&amount={self.amount}")
        # return json.loads(r.content)["result"]
        #
        # И так почему-то тоже не работает
        # r = requests.get("http://api.exchangeratesapi.io/v1/latest" +
        #                  f"?access_key={API_KEY}" +
        #                  f"&base={self.val_from}" +
        #                  f"&symbols={self.val_to})")
        # return json.loads(r.content)["rates"][self.val_to]*self.amount
        r = requests.get("http://api.exchangeratesapi.io/v1/latest" +
                         f"?access_key={API_KEY}" +
                         f"&symbols={self.val_from},{self.val_to}")
        dict_json = json.loads(r.content)
        rates = dict_json["rates"]
        # print(dict_json)
        if dict_json["base"] == self.val_from:
            return self.amount*rates[self.val_to]
        if dict_json["base"] == self.val_to:
            return self.amount/rates[self.val_from]
        return self.amount*rates[self.val_to]/rates[self.val_from]
