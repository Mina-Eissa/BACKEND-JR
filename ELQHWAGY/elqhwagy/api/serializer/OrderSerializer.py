from rest_framework import serializers
from .OrderItemSerializer import OrderItemSerializer
from ..models import Order
class OrderSerializer(serializers.Serializer):
    order_items = OrderItemSerializer(many=True, read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'employee', 'client', 'order_items', 'status', 'create_at', 'totalCost']
        read_only_fields = ['id', 'create_at', 'totalCost']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items',[])
        order_items_instances = []
        try:
            for order_item in order_items_data:
                order_item_serialzier = OrderItemSerializer(order_item)
                order_item_serialzier.is_valid(raise_exception=True)
                order_item_instance = order_item_serialzier.save()
                order_items_instances.append(order_item_instance)
        except Exception as e:
            raise str(e)
        order_instance = Order.objects.create(**validated_data)
        order_instance.order_items.set(order_items_instances)
        return order_instance
