from .models import Cart, Product


class CartManager():
    #получить экземпляр по фильтрам
    def get_cart(self, user_id, product_id):
        cart = Cart.objects.filter(user=user_id, 
                                       product=product_id).first()
        return cart
    
    def check_cart(self, user_id, cart_id):
        cart = Cart.objects.filter(pk=cart_id, user=user_id).first()
        return cart
    
    def delete_cart(self, cart_id):
        Cart.objects.delete(pk=cart_id)


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
        