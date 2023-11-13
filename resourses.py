from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
import csv
from calendar import month_abbr
from apis_to_get_currencies import get_sheqel_to_dollar_exchange_value, get_ruble_to_dollar_exchange_value

class Purchases_info:
    '''Class that takes one compulsory argument - filename of CSV file.
    CSV file should obligatory have fields named "dt_info", "paid" in order to the program processes correctly;
    currency symbol should go after a sum of money in the same field. Use standart symbols: ₽, $, ₪.
    Currency exchange values are taken from https://ru.investing.com/currencies.
    Currently program works for 3 currencies: rubles, sheqels, dollars'''

    def __init__(self, filename: str):
        self.filename = filename
        self.rub_to_usd_exchange_value = get_ruble_to_dollar_exchange_value()
        self.sheq_to_usd_exchange_value = get_sheqel_to_dollar_exchange_value()

    def total_rubles(self, start_date: date, end_date: date):
        '''Function takes 2 args: start date and end date of chosen period of time.
        Args must be of datetime.date type.
        Returns sum of payments which were paid in rubles during chosen period of time'''

        total_rubles = 0
        with open('test_data.csv', 'r', encoding='UTF-8') as file:
            info = csv.DictReader(file)
            purchases_during_period = filter(
                lambda line: start_date <= datetime.fromisoformat(line['dt_info']).date() <= end_date, info)
            for line in purchases_during_period:
                sum = line['paid']
                if '₽' in sum:
                    sum = float(sum.replace('₽', ''))
                    total_rubles += sum
        return total_rubles

    def total_dollars(self, start_date: date, end_date: date):
        '''Function takes 2 args: start date and end date of chosen period of time.
        Args must be of datetime.date type.
        Returns sum of payments which were paid in dollars during chosen period of time'''

        total_dollars = 0
        with open('test_data.csv', 'r', encoding='UTF-8') as file:
            info = csv.DictReader(file)
            purchases_during_period = filter(
                lambda line: start_date <= datetime.fromisoformat(line['dt_info']).date() <= end_date, info)
            for line in purchases_during_period:
                sum = line['paid']
                if '$' in sum:
                    sum = float(sum.replace('$', ''))
                    total_dollars += sum
        return total_dollars


    def total_sheqels(self, start_date: date, end_date: date):
        '''Function takes 2 args: start date and end date of chosen period of time.
        Args must be of datetime.date type.
        Returns sum of payments which were paid in sheqels during chosen period of time'''

        total_sheqel = 0
        with open('test_data.csv', 'r', encoding='UTF-8') as file:
            info = csv.DictReader(file)
            purchases_during_period = filter(
                lambda line: start_date <= datetime.fromisoformat(line['dt_info']).date() <= end_date, info)
            for line in purchases_during_period:
                sum = line['paid']
                if '₪' in sum:
                    sum = float(sum.replace('₪', ''))
                    total_sheqel += sum
        return total_sheqel

    def total_income_in_dollars(self, start_date: date, end_date: date):
        '''Function takes 2 args: start date and end date of chosen period of time.
        Args must be of datetime.date type.
        Returns sum of payments in all currencies during chosen period of time'''

        total = (self.total_rubles(start_date, end_date) * self.rub_to_usd_exchange_value +
                 self.total_sheqels(start_date, end_date) * self.sheq_to_usd_exchange_value +
                 self.total_dollars(start_date, end_date))
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
                   f'{round(self.total_rubles(start_date, end_date))}₽  |  '
                   f'{round(self.total_dollars(start_date, end_date))}$  |  '
                   f'{round(self.total_sheqels(start_date, end_date))}₪')
        plt.ylabel('Income')
        plt.title('Total daily income in $')
        plt.show()


