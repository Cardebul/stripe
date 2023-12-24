from django.contrib import admin
from .models import Item, Price, Order, Order_of_items, Discount, Tax
# Register your models here.


@admin.register(Price)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Item)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Order_of_items)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Discount)
class RecipeAdmin(admin.ModelAdmin):
    pass


@admin.register(Tax)
class RecipeAdmin(admin.ModelAdmin):
    pass
