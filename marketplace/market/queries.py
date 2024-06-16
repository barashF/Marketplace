from re import search
from rest_framework import status
from rest_framework.response import Response
from django.contrib.postgres.search import SearchVector

from . import managers
from . import exceptions
from . import errors
from . import serializers
from .forms import SearchForm
from .models import Product

from courier.managers import ParcelLockerManager
from courier.exceptions import NotFoundParcelLocker
from courier.errors import NotFoundFreeParcelLocker


class QueriesBasket():
    def create_basket(self, user, product):
        try:
            basket = managers.BasketManager().get_basket(user_id=user, 
                                                product_id=product)
            if basket:
                raise exceptions.NotAddedToBasket(errors.AlreadyAddedToBasket().value)
            
            data = {
                'user': user,
                'product':product
            }
            serializer_basket = serializers.BasketSerializer(data=data)
            serializer_basket.is_valid(raise_exception=True)
            serializer_basket.save()
            return Response(status=status.HTTP_201_CREATED, data={'result':'success'})

        except exceptions.NotAddedToBasket as e:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'error':str(e)})
        
    def delete_basket(self, data, user):
        try:
            basket = managers.BasketManager().check_basket(user_id=user, 
                                                           basket_id=data['basket'])
            if basket is None:
                raise exceptions.NotFoundBasket(errors.DontAddedToBasket().value)
            
            managers.BasketManager().delete_basket(basket_id=basket.pk)
            return Response(status=status.HTTP_200_OK, 
                            data={'result':'success'})
        
        except exceptions.NotFoundBasket as e:
            return Response(status=status.HTTP_404_NOT_FOUND, 
                            data={'error':str(e)})

class QueriesOrder():
    def create_order(self, data, user):
        try:
            address = ParcelLockerManager().get_free_parcel_locker(address=data['address'])
            if address is None:
                raise NotFoundParcelLocker(NotFoundFreeParcelLocker().value)
            
            products = managers.OrderProductManager().list_products(order_products=data['products'])
            if not managers.OrderManager().check_availability(products=products):
                raise exceptions.AmountProductException(errors.ShortageProduct().value)
            
            data['order_price'] = managers.OrderManager().order_price(products=products)
            data['user'] = user

            serializer_order = serializers.OrderSerializer(data=data)
            serializer_order.is_valid(raise_exception=True)
            serializer_order.save()
            return Response(status=status.HTTP_201_CREATED, 
                            data={'result':'success'})
        
        except NotFoundParcelLocker as e:
            return Response(status=status.HTTP_404_NOT_FOUND, 
                            data={'error':str(e)})
        except exceptions.AmountProductException as e:
            return Response(status=status.HTTP_403_FORBIDDEN, 
                            data={'error':str(e)})


class Search():
    def search(self, data):
        try:
            if 'query' not in data:
                raise exceptions.NotQuery(errors.DontIndicatedQuey().value)
            
            form = SearchForm(data)
            if not form.is_valid():
                raise exceptions.ErrorQuery(errors.ErrorProcessing().value)
            
            query = form.cleaned_data['query']
            products = Product.objects.annotate(
                search=SearchVector('title', 'description', 'category')
            ).filter(search=query)

            return Response(status=status.HTTP_200_OK,
                            data={'result':products})
        
        except exceptions.NotQuery as e:
            return Response(status=status.HTTP_400_BAD_REQUEST, 
                            data={'error':str(e)})
        except exceptions.ErrorQuery as e:
            return Response(status=status.HTTP_403_FORBIDDEN, 
                            data={'error':str(e)})