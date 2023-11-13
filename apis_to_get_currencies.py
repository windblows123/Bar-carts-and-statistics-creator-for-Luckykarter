import requests
import re

def get_ruble_to_dollar_exchange_value():
    currency_regex = r'\b0,\d{5}\b'
    response = requests.get('https://ru.investing.com/currencies/rub-usd').text
    value = re.search(currency_regex, response).group()
    value = float(value.replace(',', '.'))
    return value


def get_sheqel_to_dollar_exchange_value():
    currency_regex = r'\b\d,\d{4}\b'
    response = requests.get('https://ru.investing.com/currencies/ils-usd').text
    value = re.search(currency_regex, response).group()
    value = float(value.replace(',', '.'))
    return value


