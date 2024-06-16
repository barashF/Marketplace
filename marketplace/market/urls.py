from django.urls import path, include
from rest_framework import routers

from . import views

router_basket = routers.SimpleRouter()
router_basket.register(r'basket', views.BasketView)

router_order = routers.SimpleRouter()
router_order.register(r'orders', views.OrderView)


urlpatterns = [
    path('', include(router_order.urls)),
    path('', include(router_basket.urls)),
    
    path('basket/delete_basket/', views.BasketView.as_view({'delete':'delete_basket'})),
    path('product/', views.ProductView.as_view()),
    path('search/', views.ProductSearch.as_view())
]