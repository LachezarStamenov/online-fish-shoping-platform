from django.contrib import admin

from e_fish_shop_app.cart.models import Cart


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    pass
