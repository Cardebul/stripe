from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()
    currency = models.CharField(max_length=3, default='USD')

    def __str__(self):
        return self.name


class Order(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='orders')
    item = models.ManyToManyField(Item, through='Order_of_items')
    tax = models.ForeignKey(
        'Tax',
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True, null=True)
    discount = models.ForeignKey(
        'Discount',
        on_delete=models.SET_NULL,
        related_name='orders',
        blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.user.get_username()} order'


class Discount(models.Model):
    name = models.CharField(max_length=100, unique=True)
    per = models.FloatField()
    stripe_discount_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name} '


class Tax(models.Model):

    name = models.CharField(max_length=100, unique=True)
    per = models.FloatField()
    stripe_tax_id = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f'{self.name} '


class Order_of_items(models.Model):
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='orders')
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='items')
    amount = models.IntegerField(default=1)


class Price(models.Model):
    product = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='prices')
    currency = models.CharField(max_length=3, default='USD')
    stripe_price_id = models.CharField(max_length=100)
    price = models.FloatField(default=0)

    def __str__(self):
        return f'{self.product.name, self.currency, self.price}'
