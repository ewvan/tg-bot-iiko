import requests
from xml.dom.minidom import parse, parseString
import dotenv
import os
from datetime import datetime


class Revenue:
    def __init__(self, cafe):
        self.__cafe = cafe
        self.key_link = "https://kofeinya-duo-passazh.iiko.it:443/resto/api/auth"
        self.__key = self.get_key()
        self.department_link = "https://kofeinya-duo-passazh.iiko.it:443/resto/api/corporation/departments"
        self.__department = self.get_department()
        self.sales_link = "https://kofeinya-duo-passazh.iiko.it:443/resto/api/reports/sales"
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


    def get_sales(self) -> str:
        time = (datetime.now()).strftime("%d.%m.%Y")
        now = (datetime.now()).strftime("%H:%M")

        param = {
            "key": self.__key,
            "department": self.__department,
            "dateFrom": time,
            "dateTo": time
        }
        response = requests.get(self.sales_link, params=param)
        assert(response.status_code == 200)
        xml_text = parseString(response.text).getElementsByTagName('value')
        if xml_text:

            return f"Выручка {self.__cafe} на {now} {time} - {float(xml_text[0].firstChild.nodeValue):.1f} ₽"
        else:
            return "По выручке нет данных"

    def return_revenue(self):
        return self.__sales

