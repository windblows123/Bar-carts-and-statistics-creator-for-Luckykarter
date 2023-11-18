from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr
from apis_to_get_currencies import get_sheqel_to_dollar_exchange_value, get_ruble_to_dollar_exchange_value

class Purchases_info:
    '''Class that takes one compulsory argument - filename of CSV file.
    CSV file should obligatory have fields named "dt_info", "paid" in order to the program processes correctly;
    date in dt_info in CSV file must be in iso format; currency symbol should go after a sum of money in the same field.
    Use standart symbols or codes: ₽, $, ₪ or RUB, USD, ILS.
    Currency exchange values are taken from https://ru.investing.com/currencies.
    Currently program works for 3 currencies: rubles, sheqels, dollars'''

    def __init__(self, filename: str):
        self.filename = filename
        self.rub_to_usd_exchange_value = get_ruble_to_dollar_exchange_value()
        self.sheq_to_usd_exchange_value = get_sheqel_to_dollar_exchange_value()


    def total_currencies(self, start_date: date, end_date: date) ->tuple[int]:
        total_rubles = 0
        total_dollars = 0
        total_sheqels = 0
        with open('test_data.csv', 'r', encoding='UTF-8') as file:
            info = csv.DictReader(file)
            purchases_during_period = filter(
                lambda line: start_date <= datetime.fromisoformat(line['dt_info']).date() <= end_date, info)
            for line in purchases_during_period:
                amount_of_money = line['paid']
                if ('₽' or 'RUB') in amount_of_money:
                    amount_of_money = float(amount_of_money.replace('₽', '').replace('RUB', ''))
                    total_rubles += amount_of_money
                elif ('$' or 'USD') in amount_of_money:
                    amount_of_money = float(amount_of_money.replace('$', '').replace('USD', ''))
                    total_dollars += amount_of_money
                elif ('₪' or 'ILS') in amount_of_money:
                    amount_of_money = float(amount_of_money.replace('₪', '').replace('ILS', ''))
                    total_sheqels += amount_of_money
        return (total_rubles, total_dollars, total_sheqels)

    def total_income_in_dollars(self, start_date: date, end_date: date):
        '''Function takes 2 args: start date and end date of chosen period of time.
        Args must be of datetime.date type.
        Returns sum of payments in all currencies during chosen period of time'''

        total_rubles, total_dollars, total_sheqels = self.total_currencies(start_date, end_date)
        self.dollars = total_dollars
        self.rubles = total_rubles
        self.sheqels = total_sheqels
        total = (total_rubles * self.rub_to_usd_exchange_value +
                 total_sheqels * self.sheq_to_usd_exchange_value +
                 total_dollars)
        return total

    def drow_a_bar_chart(self, start_date: date, end_date: date):
        '''Draws a bar chart of total income in dollars for chosen period of time'''

        temp_date = start_date
        interval = [start_date]
        while temp_date != end_date:
            temp_date += timedelta(days=1)
            interval.append(temp_date)

        x_axis = list(map(lambda dt: str(dt)[-2:] + '\n' + month_abbr[dt.month], interval))
        y_axis = []
        for day in interval:
            day_total_income = self.total_income_in_dollars(day, day)
            y_axis.append(day_total_income)
        plt.bar(x_axis, y_axis, label=f'Income rates in $')
        plt.legend()
        plt.xlabel(f'Dates\nTOTAL: {round(self.total_income_in_dollars(start_date, end_date))} USD PAID IN CURRENCIES: '
                   f'{round(self.rubles)}₽  |  '
                   f'{round(self.dollars)}$  |  '
                   f'{round(self.sheqels)}₪')
        plt.ylabel('Income')
        plt.title('Total daily income in $')
        plt.show()



