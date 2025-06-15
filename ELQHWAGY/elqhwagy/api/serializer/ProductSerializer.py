from rest_framework import serializers
from ..models import Product, Ingredient, ProductIngredient
from .IngredientSerializer import IngredientSerializer
from .ProductIngredientSerializer import ProductIngredientInputSerializer, ProductIngredientOutputSerializer


class ProductSerializer(serializers.ModelSerializer):
    ingredients = ProductIngredientInputSerializer(many=True, write_only=True)
    product_ingredients = serializers.SerializerMethodField()
    created_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_at = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S", read_only=True)
    stockCount = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_stockCount(self, obj):
        return obj.stockCount

    def get_product_ingredients(self, obj):
        product_ingredients_instances = ProductIngredient.objects.filter(
            product=obj)
        return ProductIngredientOutputSerializer(product_ingredients_instances, many=True).data

    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients', [])
        product_instance = Product.objects.create(**validated_data)

        for ingredient_data in ingredients_data:
            # Fetch or create the ingredient
            ingredient, _ = Ingredient.objects.get_or_create(
                name=ingredient_data['name'],
                type=ingredient_data['type']
            )
            # Create the link through ProductIngredient
            ProductIngredient.objects.create(
                product=product_instance,
                ingredient=ingredient,
                weight=ingredient_data.get('weight'),
                unit_count=ingredient_data.get('unit_count')
            )

        return product_instance
