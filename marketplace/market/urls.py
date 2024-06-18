from django.urls import path, include
from rest_framework import routers

from . import views

router_basket = routers.SimpleRouter()
router_basket.register(r'cart', views.CartView)

router_order = routers.SimpleRouter()
router_order.register(r'orders', views.OrderView)


urlpatterns = [
    path('', include(router_order.urls)),
    path('', include(router_basket.urls)),
    
    path('cart/delete_cart/', views.CartView.as_view({'delete':'delete_cart'})),
    path('product/', views.ProductView.as_view()),
    path('search/', views.ProductSearch.as_view())
]