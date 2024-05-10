class DatabaseError(Exception):
    def __init__(self):
        super().__init__("error while working with the database")


class EmptyFieldError(Exception):
    def __init__(self):
        super().__init__("Field shouldn't be empty")


class LongFieldError(Exception):
    def __init__(self):
        super().__init__("Field shouldn't be longer than 32")


