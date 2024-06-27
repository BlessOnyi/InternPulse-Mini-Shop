from rest_framework import serializers
from .models import Product,Order

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'product','name', 'quantity', 'order_date']  

    def create(self, validated_data):
        validated_data['canceled'] = False  
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if 'canceled' in validated_data:
            validated_data.pop('canceled')  
        return super().update(instance, validated_data)