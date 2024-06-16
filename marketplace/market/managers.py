from .models import Basket, Product


class BasketManager():
    #получить экземпляр по фильтрам
    def get_basket(self, user_id, product_id):
        basket = Basket.objects.filter(user=user_id, 
                                       product=product_id).first()
        return basket
    
    def check_basket(self, user_id, basket_id):
        basket = Basket.objects.filter(pk=basket_id, user=user_id).first()
        return basket
    
    def delete_basket(self, basket_id):
        Basket.objects.delete(pk=basket_id)


class OrderProductManager():
    #список (Product, amount)
    def list_products(self, order_products):
        products = []
        for product_order in order_products:
            product = Product.objects.get(pk=product_order['product'])
            products.append((product, product_order['amount']))

        return products
    

class OrderManager():
    #Общая сумма заказа, products массив вида [(product, ...), (product, ...)]
    def order_price(self, products):
        price = 0
        for product_order in products:
            price += product_order[0].price * product_order[1]
        
        return price
    
    #Проверка на наличие в магазине
    def check_availability(self, products):
        for product in products:
            if product[0].storage < product[1]:
                return False
        return True
        