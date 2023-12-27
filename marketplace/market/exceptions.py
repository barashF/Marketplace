class BaseException(Exception):
    def __init__(self, text):
        self.text = text
        super().__init__(text)


class NotAddedToBasket(BaseException):
    pass