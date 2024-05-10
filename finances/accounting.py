from datetime import date, datetime
from typing import Literal


class Purchase:
    def __init__(self, name: str, date_purchase: date, category: str, price: float):
        self.name = name
        self.date_purchase = date_purchase
        self.category = category
        self.price = price


class Operation:
    def __init__(self, summ: float, date_time: datetime = datetime.now(),
                 type: Literal["Пополнение", "Списание", "Возврат товара"] = "Списание"):
        self.summ = summ
        self.date_time = date_time
        self.type = type

