from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Client, Product, Ingredient, Order, ProductIngredient

admin.site.register(Client)

admin.site.register(Ingredient)


class ProductIngredientInlineForm(forms.ModelForm):
    class Meta:
        model = ProductIngredient
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ingredient = getattr(self.instance, 'ingredient', None)

        if ingredient:
            if ingredient.type == Ingredient.IngredientType.COUNTABLE:
                self.fields['weight'].widget = forms.HiddenInput()
            elif ingredient.type == Ingredient.IngredientType.UNCOUNTABLE:
                self.fields['unit_count'].widget = forms.HiddenInput()


class ProductIngredientInline(admin.TabularInline):
    model = Product.ingredients.through
    # form = ProductIngredientInlineForm
    extra = 1


class OrderItemInline(admin.TabularInline):
    model = Order.order_items.through
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'category',
                    'created_at', 'updated_at', 'stockCount')
    search_fields = ('name', 'category')
    readonly_fields = ('created_at', 'updated_at', 'stockCount')
    inlines = [ProductIngredientInline]

    fieldsets = (
        (None, {'fields': ('name', 'price', 'category')}),
        (None, {'fields': ('created_at', 'updated_at', 'stockCount')}),
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'employee', 'client',
                    'status', 'create_at', 'totalCost')
    search_fields = ('employee__username', 'client__username', 'status')
    readonly_fields = ('create_at', 'totalCost')
    inlines = [OrderItemInline]

    fieldsets = (
        (None, {'fields': ('employee', 'client', 'status')}),
        (None, {'fields': ('create_at', 'totalCost')}),
    )


@admin.register(User)
class UserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'is_staff',
                    'is_superuser', 'date_joined')
    search_fields = ('username', 'email', 'phone_numbers')
    readonly_fields = ('date_joined',)

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('phone_numbers', 'profile_img')}),
    )
