import uuid
from django.db import models
from django.utils.timezone import now
from django.core.exceptions import ValidationError


class Ingredient(models.Model):
    class IngredientType(models.TextChoices):
        COUNTABLE = 'COUNTABLE', 'COUNTABLE'
        UNCOUNTABLE = 'UNCOUNTABLE', 'UNCOUNTABLE'
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100,unique=True,verbose_name="ingredient name")
    type = models.TextField(verbose_name='ingredient type',
                            choices=IngredientType.choices, default=IngredientType.COUNTABLE)
    stock_weight = models.FloatField(default=0.0,verbose_name ="stock weight")
    stock_unit_count = models.IntegerField(default=0,verbose_name="stock units")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    
    def increaseStock(self,amount):
        if self.type == Ingredient.IngredientType.COUNTABLE:
            self.stock_unit_count += amount
        elif self.type == Ingredient.IngredientType.UNCOUNTABLE:
            self.stock_weight += amount
    
    def decreaseStock(self,amount):
        if self.type == Ingredient.IngredientType.COUNTABLE:
            self.stock_unit_count -= min(amount,self.stock_unit_count)
        elif self.type == Ingredient.IngredientType.UNCOUNTABLE:
            self.stock_weight -= min(amount,self.stock_weight)
