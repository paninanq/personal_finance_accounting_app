class PriceLessZero(Exception):
    def __init__(self):
        super().__init__("Price should be less than zero")


class DateError(Exception):
    def __init__(self):
        super().__init__("Date shouldn't be later than today")
        
        
class BalanceLessZero(Exception):
    def __init__(self):
        super().__init__("Insufficient funds")


class SummLessZero(Exception):
    def __init__(self):
        super().__init__("Summ should be less than zero")
