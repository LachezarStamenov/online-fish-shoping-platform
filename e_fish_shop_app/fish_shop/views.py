from django.shortcuts import render

from e_fish_shop_app.store.models import Product


def home(request):
    products = Product.objects.all().filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'index.html', context)


