from .models import Product, ImageProduct, Cart, Order, OrderProduct
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


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['user', 'product']


class OrderProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = OrderProduct
        fields = ['product', 'amount', 'order']


class OrderSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['products', 'user', 'parcel_locker', 
                  'status', 'courier', 'order_price']
    
    def create(self, validated_data):
        products = validated_data.pop('products')
        order = Order.objects.create(**validated_data)
        for product in products:
            OrderProduct.objects.create(order=order, **product)
        
        return order