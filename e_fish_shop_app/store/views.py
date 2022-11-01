from django.shortcuts import render, get_object_or_404
from django.views import generic as views

from e_fish_shop_app.category.models import Category
from e_fish_shop_app.store.models import Product


def store(request, category_slug=None):
    categories = None
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        products_count = len(Product.objects.all().filter(is_available=True))
    else:
        products = Product.objects.all().filter(is_available=True)
        products_count = len(Product.objects.all().filter(is_available=True))

    context = {
        'products': products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)
