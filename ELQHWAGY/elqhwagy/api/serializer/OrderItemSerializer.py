from rest_framework import serializers
from ..models import OrderItem
class OrderItemSerializer(serializers.Serializer):
    product_name= serializers.CharField(source='product.name',read_only=True)
    product_price = serializers.DecimalField(source='product.price',max_digits=10,decimal_places=2,read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    class Meta:
        model = OrderItem
        feilds = ['id','product_name','product_price','quantity','create_at','total']