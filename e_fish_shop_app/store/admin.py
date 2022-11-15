import admin_thumbnails
from django.contrib import admin

from e_fish_shop_app.store.models import Product, Variation, ReviewRating, ProductGallery


@admin_thumbnails.thumbnail('image')
class ProductGalleryInline(admin.TabularInline):
    model = ProductGallery
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'stock', 'category', 'modified_date', 'is_available')
    prepopulated_fields = {'slug': ('product_name',)}
    inlines = [ProductGalleryInline]


@admin.register(Variation)
class VariationAdmin(admin.ModelAdmin):
    list_display = ('product', 'variation_category', 'variation_value', 'is_active')
    list_editable = ('is_active',)  # make the check button be active in admin
    list_filter = ('product', 'variation_category', 'variation_value')  # make a filtering able in admin for these
    # fields


@admin.register(ReviewRating)
class ReviewRatingAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    pass


