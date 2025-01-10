import time
from xml.etree import ElementTree as ET

import matplotlib.pyplot as plt
import requests


class CurrencyFetcher:
    def __init__(self, min_interval=1):
        self.currencies_ids_lst = []
        self.result = []
        self.last_request_time = 0
        self.min_interval = min_interval

    def set_currencies_ids(self, currencies_ids_lst):
        self.currencies_ids_lst = currencies_ids_lst

    def get_result(self):
        return self.result

    def fetch_currencies(self):
        current_time = time.time()
        if current_time - self.last_request_time < self.min_interval:
            raise Exception("Requests are being made too frequently.")

        self.last_request_time = current_time
        cur_res_str = requests.get('https://www.cbr.ru/scripts/XML_daily.asp')
        root = ET.fromstring(cur_res_str.content)
        valutes = root.findall("Valute")

        self.result = []
        for _v in valutes:
            valute_id = _v.get('ID')
            if str(valute_id) in self.currencies_ids_lst:
                valute_cur_name = _v.find('Name').text
                valute_cur_val = _v.find('Value').text
                valute_charcode = _v.find('CharCode').text
                valute_nominal = _v.find('Nominal').text
                valute = {
                    'id': valute_id,
                    'name': valute_cur_name,
                    'value': float(valute_cur_val.replace(',', '.')),
                    'charcode': valute_charcode,
                    'nominal': int(valute_nominal)
                }
                self.result.append(valute)

        if not self.result:
            self.result = [{'R9999': None}]

    def visualize_currencies(self):
        if not self.result:
            raise Exception("No data to visualize.")

        fig, ax = plt.subplots()
        currencies = [valute['charcode'] for valute in self.result]
        values = [valute['value'] for valute in self.result]

        ax.bar(currencies, values)
        ax.set_ylabel('Цена в рублях')
        ax.set_title('Currency Exchange Rates')
        plt.savefig('currencies.jpg')
        plt.show()

    def print_formatted_result(self):
        formatted_result = [
            {valute['charcode']: (valute['name'], valute['value'])}
            for valute in self.result
        ]
        print(formatted_result)


if __name__ == "__main__":
    fetcher = CurrencyFetcher()
    fetcher.set_currencies_ids(['R01035', 'R01239', 'R01235'])
    fetcher.fetch_currencies()
    fetcher.visualize_currencies()
    fetcher.print_formatted_result()