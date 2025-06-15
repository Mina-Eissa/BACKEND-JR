from rest_framework import serializers
from ..models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    amount = serializers.SerializerMethodField(read_only=True)
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)

    def get_amount(self, obj):
        if obj.type == Ingredient.IngredientType.COUNTABLE:
            return f"{obj.stock_unit_count} piece"
        else:
            return f"{obj.stock_weight} gm"

    class Meta:
        model = Ingredient
        fields = '__all__'
