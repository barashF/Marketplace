from .models import Basket


class BasketManager():
    #получить экземпляр по фильтрам
    def get_basket(self, user_id, product_id):
        basket = Basket.objects.filter(user=user_id, 
                                       product=product_id).first()
        return basket
    
    def delete_basket(self, basket_id):
        Basket.objects.delete(pk=basket_id)
    
    