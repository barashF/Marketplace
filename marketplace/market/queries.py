from rest_framework import status
from rest_framework.response import Response

from .managers import BasketManager
from .exceptions import NotAddedToBasket
from .error import AlreadyAddedToBasket
from .api.serializers import BasketSerializer

class QueriesBasket():
    def create_basket(self, user, product):
        try:
            basket = BasketManager().get_basket(user_id=user, 
                                                product_id=product)
            if basket:
                raise NotAddedToBasket(AlreadyAddedToBasket().value)
            
            data = {
                'user': user,
                'product':product
            }
            serializer_basket = BasketSerializer(data=data)
            serializer_basket.is_valid(raise_exception=True)
            serializer_basket.save()
            return Response(status=status.HTTP_201_CREATED, data={'result':'success'})

        except NotAddedToBasket as e:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error':str(e)})
        

