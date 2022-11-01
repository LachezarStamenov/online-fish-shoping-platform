from django.contrib import admin

from e_fish_shop_app.accounts.models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    pass
