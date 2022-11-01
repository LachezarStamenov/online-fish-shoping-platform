from django.contrib import admin

from e_fish_shop_app.category.models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass

