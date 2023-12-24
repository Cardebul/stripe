from django.contrib import admin

from .models import Discount, Item, Order, Order_of_items, Price, Tax


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
