from django.shortcuts import render, get_object_or_404
from django.views import generic as views
from e_fish_shop_app.cart.helpers import _get_cart_id
from e_fish_shop_app.cart.models import CartItem
from e_fish_shop_app.category.models import Category
from e_fish_shop_app.store.models import Product


class StoreView(views.DetailView):
    model = Product
    template_name = 'store/store.html'
    context_object_name = 'products'
    def get_object(self, queryset=None):
        if 'category_slug' in self.kwargs:
            self.categories = get_object_or_404(Category, slug=self.kwargs['category_slug'])
            self.products = Product.objects.all().filter(category=self.categories, is_available=True)
        else:
            self.products = Product.objects.all().filter(is_available=True)
        return self.products

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'category_slug' in self.kwargs:
            context['products_count'] = Product.objects.all().filter(category=self.categories, is_available=True).count()
        else:
            context['products_count'] = Product.objects.all().filter(is_available=True).count()
        return context


def show_product_details(request, category_slug, product_slug):
    """Show the product details information"""
    try:
        product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        is_in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(request), product=product).exists()
    except Exception as ex:
        raise ex
    context = {
        'product': product,
        'is_in_cart': is_in_cart
    }
    return render(request, 'store/product_details.html', context)