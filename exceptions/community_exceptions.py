class DateRefillError(Exception):
    def __init__(self):
        super().__init__("You can top up your account only on the first day of the month")


class PriceLessZero(Exception):
    def __init__(self):
        super().__init__("Price should be less than zero")
        
        
class BalanceLessZero(Exception):
    def __init__(self):
        super().__init__("Insufficient funds")
