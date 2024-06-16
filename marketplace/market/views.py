from unittest import result
from rest_framework.viewsets import ViewSet
from rest_framework import views
from rest_framework.permissions import AllowAny
from rest_framework import generics, mixins, status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, OpenApiRequest
from drf_spectacular.types import OpenApiTypes
from rest_framework.response import Response
from rest_framework.decorators import action


from .models import Product, Basket, Order
from .forms import SearchForm
from . import serializers
from . import queries



@extend_schema(tags=['Products'], )
class ProductView(generics.GenericAPIView,
                    mixins.ListModelMixin):
    queryset = Product.objects.all()
    serializer_class = serializers.ProductSerializer
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
    queryset = Order.objects.all()

    @extend_schema( 
        tags=['Basket'],
        description='Добавить товар в корзину',
        request=OpenApiRequest(OpenApiExample(name='Example add to basket')),
        responses={201: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example add to basket', 
                                 value={'result': 'success'}, 
                                response_only=True, 
                                status_codes=[201]),
                OpenApiExample(name='Example add to basket', value={'error': 'error_message'}, 
                                response_only=True, 
                                status_codes=[403]),
                OpenApiExample(name='Example add to basket', 
                                value={'product': '1'}, 
                                request_only=True)
        ],
    )
    @action(methods=['post'], detail=False)
    def add_basket(self, request):
        response = queries.QueriesBasket().create_basket(user=request.user.pk, 
                                                 product=request.data['product'])
        return response
    
    @extend_schema(description='Получить корзину пользователя',
                   responses={200: serializers.BasketSerializer},
        examples=[OpenApiExample(name='Example get basket', 
                                 value={'error':'message'}, 
                                 response_only=True, 
                                 status_codes=[404]),],)
    @action(methods=['get'], detail=False)
    def list_basket(self, request):
        queryset = Basket.objects.filter(user=request.user.pk)
        serializer_class = serializers.BasketSerializer(queryset, many=True)
        return Response(status=status.HTTP_200_OK, 
                        data={'result':serializer_class.data})
    
    @extend_schema(
        description='Удалить товар из корзины',
        parameters=[OpenApiParameter(name='basket', description='id basket', required=True, type=int),],
        request=OpenApiRequest(),
        responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example delete basket', 
                                 value={'result':'success'}, 
                                 response_only=True, 
                                 status_codes=[200]),
                  OpenApiExample(name='Example delete basket', 
                                 value={'error':'message'}, 
                                 response_only=True, 
                                 status_codes=[404]),
        ],
    )
    def delete_basket(self, request):
        response = queries.QueriesBasket().delete_basket(data=request.data, 
                                                         user=request.user)
        return response


@extend_schema(tags=['Orders'])
class OrderView(ViewSet):
    queryset = Order.objects.all()
    
    @extend_schema( 
        description='Сделать заказ',
        request=OpenApiExample(name='Example create order'),
        responses={201: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
        examples=[OpenApiExample(name='Example create order', 
                                 value={'result': 'success'}, 
                                response_only=True, 
                                status_codes=[201]),
                OpenApiExample(name='Example create order', value={'error': 'error_message'}, 
                                response_only=True, 
                                status_codes=[403]),
                OpenApiExample(name='Example create order', 
                                value={'address':'example address',
                                      'products':[
                                           {
                                            'product':1,
                                            'amount':2
                                           },
                                           {
                                            'product':1,
                                            'amount':2
                                           }
                                      ]}, 
                                request_only=True)
        ],
    )
    @action(methods=['post'], detail=False)
    def create_order(self, request):
        response = queries.QueriesOrder().create_order(data=request.data, 
                                                       user=request.user.pk)
        return response


class ProductSearch(views.APIView):
    permission_classes = [AllowAny]

    def get(request):
        response = queries.Search().search(request.GET)
        return response


