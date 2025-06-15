
import uuid
from django.db import models
from django.utils.timezone import now
from .Choices import Categories
from django.core.exceptions import ValidationError
from .Ingredient import Ingredient


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    ingredients = models.ManyToManyField(
        Ingredient, through='ProductIngredient', related_name='product_ingredients')
    category = models.CharField(
        max_length=10, choices=Categories.choices, default=Categories.DRINK)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.price < 0:
            raise ValidationError("Price must not be negative.")

    @property
    def stockCount(self):
        units = []
        PIs = ProductIngredient.objects.filter(
            product_id=self.id).select_related('ingredient')

        for pi in PIs:
            stock = pi.ingredient
            if pi.ingredient.type == Ingredient.IngredientType.COUNTABLE:
                if stock.stock_unit_count is None or pi.weight or pi.unit_count == 0:
                    return 0
                units.append(stock.stock_unit_count // pi.unit_count)

            elif pi.ingredient.type == Ingredient.IngredientType.UNCOUNTABLE:
                if stock.stock_weight is None or pi.weight is None or pi.weight == 0:
                    return 0
                units.append(stock.stock_weight // pi.weight)
        return int(min(units)) if units else 0

    def __str__(self):
        return f"{self.name} ({self.category}) - {self.price} EGP"


class ProductIngredient(models.Model):
    id = models.AutoField(
        primary_key=True, editable=False, verbose_name='PIID')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_ingredients')
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, related_name='ingredient_products')
    weight = models.FloatField(null=True, blank=True, verbose_name="weight")
    unit_count = models.PositiveIntegerField(
        null=True, blank=True, verbose_name="units")

    def clean(self):
        # Enforce business rule: one and only one field must be filled based on type
        if self.ingredient.type == Ingredient.IngredientType.COUNTABLE:
            if self.unit_count is None:
                raise ValidationError(
                    "Countable ingredients must have 'unit_count'.")
            if self.weight is not None:
                raise ValidationError(
                    "Countable ingredients should not have 'weight'.")
        elif self.ingredient.type == Ingredient.IngredientType.UNCOUNTABLE:
            if self.weight is None:
                raise ValidationError(
                    "Uncountable ingredients must have 'weight'.")
            if self.unit_count is not None:
                raise ValidationError(
                    "Uncountable ingredients should not have 'unit_count'.")
