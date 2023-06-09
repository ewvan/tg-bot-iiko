import requests
from xml.dom.minidom import parse, parseString
import dotenv
import os
import datetime
from pytz import timezone
import json

class Lfl:
    def __init__(self, cafe: str, cafe_link: str, yesterday:bool = False) -> None:
        self.yesterday = yesterday
        self.__cafe = cafe
        self.key_link = f"{cafe_link}/resto/api/auth"
        self.__key = self.get_key()
        self.department_link = f"{cafe_link}/resto/api/corporation/departments"
        self.__department = self.get_department()
        self.sales_link = f"{cafe_link}/resto/api/reports/sales"
        self.__sales = self.get_sales()

    def get_key(self) -> str:
        dotenv.load_dotenv()
        response = requests.get(self.key_link,params={
            "login": os.getenv("LOGIN"),
            "pass": os.getenv("PASS")
        })

        return response.text

    def get_department(self) -> str:
        response = requests.get(self.department_link, params={"key": self.__key})
        assert(response.status_code == 200)

        xml_text = parseString(response.text)
        document = xml_text.getElementsByTagName("corporateItemDto")
        return [i.getElementsByTagName("id")[0].firstChild.nodeValue for i in document if (self.__cafe in i.getElementsByTagName("name")[0].firstChild.nodeValue and i.getElementsByTagName("type")[0].firstChild.nodeValue == "DEPARTMENT")][0]

    def get_sales_info(self, latency: int = 0) -> json:
        time_zone = 'Asia/Yekaterinburg'

        today = datetime.datetime.now(timezone(time_zone)) - datetime.timedelta(days=latency)

        time = today.strftime("%d.%m.%Y")
        now = today.strftime("%H:%M")
        param = {
            "key": self.__key,
            "department": self.__department,
            "dateFrom": time,
            "dateTo": time,
            "hourTo": now[0:2] if not self.yesterday else -1,
            "hourFrom": "0" if not self.yesterday else -1,
            "dishDetails": True
        }

        response = requests.get(self.sales_link, params=param)
        assert (response.status_code == 200)
        xml_response = parseString(response.text).getElementsByTagName('dayDishValue')
        check_count = len(xml_response)
        revenue_sum = sum([float(_.getElementsByTagName('value')[0].firstChild.nodeValue) for _ in xml_response])
        data = {
            "revenue": revenue_sum,
        }

        return data


    def get_sales(self) -> str:
        if not self.yesterday:
            today: json = self.get_sales_info(0)
            week_ago: json = self.get_sales_info(7)
        else:
            today: json = self.get_sales_info(1)
            week_ago: json = self.get_sales_info(8)
        if today and week_ago and week_ago["revenue"] != 0:
            lfl_coeff = (today["revenue"] - week_ago["revenue"]) / week_ago["revenue"] * 100
            return f"<u>{self.__cafe}</u>\n<b>Like for Like:</b> {'+' if lfl_coeff > 0 else ''}{lfl_coeff:.2f}%\n"

        else:
            return f"По <u>{self.__cafe}</u> нет данных"

    def return_revenue(self):
        return self.__sales

