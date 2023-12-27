from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import generics, mixins, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiResponse, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response

from ..models import Market, Product, Basket, Order
from .serializers import ProductSerializer, BasketSerializer, OrderSerializer
from ..queries import QueriesBasket
from ..managers import BasketManager


@extend_schema(tags=['Products'], )
class ProductView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        queryset = Product.objects.all()
        filter = {}
        for i in self.request.GET.keys():
            if i != 'page':
                filter[i] = self.request.GET[i]
        return queryset.filter(**filter)
    
    @extend_schema(description='Получение товаров')
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@extend_schema(tags=['Basket'])
class BasketView(ViewSet):
    @extend_schema( 
        tags=['Basket'],
        description='Добавить товар в корзину',
        request=OpenApiRequest(OpenApiExample(name='Example add to basket')),
        responses={201: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example add to basket', value={'result': 'success'}, 
                                response_only=True, status_codes=[201]),
                OpenApiExample(name='Example add to basket', value={'error': 'error_message'}, 
                                response_only=True, status_codes=[403]),
                OpenApiExample(name='Example add to basket', 
                                value={'product': '1'}, request_only=True)
        ],
    )
    def create(self, request):
        response = QueriesBasket().create_basket(user=request.user.pk, 
                                                 product=request.data['product'])
        return response
    
    @extend_schema(description='Получить корзину пользователя',
                   responses={200: BasketSerializer},
        examples=[OpenApiExample(name='Example get basket', value={'error':'message'}, response_only=True, status_codes=[404]),],)
    def list(self, request):
        queryset = Basket.objects.filter(user=request.user.pk)
        serializer_class = BasketSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, data={'result':serializer_class.data})
    
    @extend_schema(
        description='Удалить товар из корзины',
        parameters=[OpenApiParameter(name='basket', description='id товара в корзине', required=True, type=int),],
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example delete basket', value={'result':'success'}, response_only=True, status_codes=[200]),
                  OpenApiExample(name='Example delete basket', value={'error':'message'}, response_only=True, status_codes=[404]),
        ],
    )
    def destroy(self, request):
        BasketManager().delete_basket(basket_id=request.GET.get('basket'))
        return Response(status=status.HTTP_200_OK, data={'result': 'success'})


@extend_schema(tags=['Orders'])
class OrderView(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_fields = ['pk', 'user']