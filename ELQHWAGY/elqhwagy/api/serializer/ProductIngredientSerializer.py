from rest_framework import serializers
from ..models import ProductIngredient,Ingredient
from .IngredientSerializer import IngredientSerializer

class ProductIngredientInputSerializer(serializers.Serializer):
    name = serializers.CharField()
    type = serializers.CharField()
    weight = serializers.FloatField(required=False)
    unit_count = serializers.IntegerField(required=False)


class ProductIngredientOutputSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)
    name = serializers.CharField(source='ingredient.name')
    type = serializers.CharField(source='ingredient.type')
    def get_amount(self, obj):
        if obj.ingredient.type == Ingredient.IngredientType.COUNTABLE:
            return f"{obj.unit_count} piece"
        else:
            return f"{obj.weight} gm"
    class Meta:
        model = ProductIngredient
        fields = ['id', 'name', 'type','amount']

