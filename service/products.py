import requests
import dotenv
import os
import datetime

class Products:
    def __init__(self, cafe: str, cafe_link: str):
        self.__cafe = cafe
        self.key_link = f"{cafe_link}/resto/api/auth"
        self.__key = self.get_key()
        self.__cafe_link = f"{cafe_link}/resto/api/v2/documents/writeoff"
        self.__products_data = self.get_products_data()


    def get_key(self) -> str:
        dotenv.load_dotenv()
        response = requests.get(self.key_link,params={
            "login": os.getenv("LOGIN"),
            "pass": os.getenv("PASS")
        })

        return response.text

    def get_products_data(self):
        date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
        param = {
            "key": self.__key,
            "dateFrom": date,
            "dateTo": date
        }

        response = requests.get(self.__cafe_link, params=param)
        assert (response.status_code == 200)
        array_data = response.json()

        output_data = {}
        if array_data['result'] == 'SUCCESS':
            details = array_data['response']
            accounts = set([i['accountId'] for i in details])
            for account in accounts:
                output_data[account] = {
                    "cost": 0,
                    "count": 0
                }

            for account in accounts:
                for detail in details:
                    if detail['accountId'] == account:
                        for item in detail['items']:
                            output_data[account]['cost'] = item['cost']
                            output_data[account]['count'] += 1

        if len(output_data) > 0:
            result = f"{self.__cafe}: \n"
            for a,b in output_data.items():
                result += f"Информация о списаниях за вчера по счету {a} в количестве {int(b['count'])} на сумму {float(b['cost']):.1f}₽\n"

            return result
        else:
            return f"По {self.__cafe} нет данных"


    def return_products(self):
        return self.__products_data
