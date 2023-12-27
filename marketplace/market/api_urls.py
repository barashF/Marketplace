from django.urls import path, include
from rest_framework import routers

from .api.views_api import ProductView, BasketView, OrderView


router_order = routers.SimpleRouter()
router_order.register(r'orders', OrderView)

urlpatterns = [
    path('', include(router_order.urls)),
    
    path('product/', ProductView.as_view()),
    path('basket/', BasketView.as_view({'get':'list',
                                        'post':'create',
                                        'delete':'destroy'})),
]