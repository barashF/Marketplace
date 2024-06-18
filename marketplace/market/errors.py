class AlreadyAddedToCart():
    def __init__(self):
        self.value = 'Товар уже добавлен в корзину'


class ShortageProduct():
    def __init__(self):
        self.value = 'На складе недостаточно товара'


class DontAddedToCart():
    def __init__(self):
        self.value = 'Товар не найден в корзине'


class DontIndicatedQuey():
    def __init__(self):
        self.value = 'Не указан запрос'


class ErrorProcessing():
    def __init__(self):
        self.value = 'Ошибка при обработке запроса'