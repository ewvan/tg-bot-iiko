import requests
from xml.dom.minidom import parse, parseString
import dotenv
import os
import datetime


class Discount:
    def __init__(self, cafe: str, cafe_link: str):
        self.__cafe = cafe
        self.key_link = f"{cafe_link}/resto/api/auth"
        self.__key = self.get_key()
        self.discount_link = f"{cafe_link}/resto/api/reports/olap"
        self.__discount_sum = self.get_discount()

    def get_key(self) -> str:
        dotenv.load_dotenv()
        response = requests.get(self.key_link, params={
            "login": os.getenv("LOGIN"),
            "pass": os.getenv("PASS")
        })

        return response.text

    def get_discount(self) -> str:
        date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d.%m.%Y")

        param = {
            "key": self.__key,
            "report": "SALES",
            "agr": "DiscountSum",
            "from": date,
            "to": date
        }

        response = requests.get(self.discount_link,params=param)
        assert (response.status_code == 200)

        value = float(parseString(response.text).getElementsByTagName('DiscountSum')[0].firstChild.nodeValue)
        return f"Себестоимость скидки за вчера в {self.__cafe} составляет {value:.1f}₽"

    def return_discount(self):
        return self.__discount_sum

