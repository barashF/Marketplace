from ..models import Product, ImageProduct, Basket, Order
from rest_framework import serializers


class ImageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageProduct
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    images = ImageProductSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'market', 'images',
                  'category', 'price', 'storage', 'image']


class BasketSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Basket
        fields = ['user', 'product']


class OrderSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['products', 'user', 'parcel_locker', 
                                    'status', 'courier']