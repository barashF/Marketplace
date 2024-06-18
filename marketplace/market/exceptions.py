class BaseException(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)


class NotAddedToCart(BaseException):
    pass


class AmountProductException(BaseException):
    pass


class NotFoundCart(BaseException):
    pass


class NotQuery(BaseException):
    pass


class ErrorQuery(BaseException):
    pass