from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from e_fish_shop_app.cart.helpers import _get_cart_id
from e_fish_shop_app.cart.models import CartItem
from e_fish_shop_app.category.models import Category
from e_fish_shop_app.store.models import Product
from django.views import generic as views


def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, 3)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


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


class SearchView(views.ListView):
    model = Product
    template_name = 'store/store.html'

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        queryset = Product.objects.all()
        if keyword:
            queryset = queryset.order_by('-created_date').filter(
                Q(description__icontains=keyword) | Q(product_name__icontains=keyword)
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.object_list:
            context['products_count'] = self.object_list.count
            context['products'] = self.object_list
            return context
