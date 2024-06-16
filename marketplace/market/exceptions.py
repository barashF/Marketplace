from unittest.mock import Base


class BaseException(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)


class NotAddedToBasket(BaseException):
    pass


class AmountProductException(BaseException):
    pass


class NotFoundBasket(BaseException):
    pass


class NotQuery(BaseException):
    pass


class ErrorQuery(BaseException):
    pass