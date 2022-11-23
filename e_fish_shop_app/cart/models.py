from django.core.validators import MinValueValidator
from django.db import models

from e_fish_shop_app.accounts.models import Account
from e_fish_shop_app.store.models import Product, Variation


class Cart(models.Model):
    cart_id = models.CharField(max_length=200, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    """Cart items model which keep information for the item details within the cart"""
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ('product',)

    def sub_total_price(self):
        """Return calculation of total price for an item based on the quantity"""
        return self.product.price * self.quantity

    def __unicode__(self):
        return self.product

