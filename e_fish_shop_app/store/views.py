from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from e_fish_shop_app.cart.helpers import _get_cart_id
from e_fish_shop_app.cart.models import CartItem
from e_fish_shop_app.category.models import Category
from e_fish_shop_app.orders.models import OrderProduct
from e_fish_shop_app.store.forms import ReviewForm
from e_fish_shop_app.store.models import Product, ReviewRating
from django.views import generic as views

NUMBER_OF_PRODUCTS_PER_PAGE = 3

def store(request, category_slug=None):
    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
        paginator = Paginator(products, NUMBER_OF_PRODUCTS_PER_PAGE)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(products, NUMBER_OF_PRODUCTS_PER_PAGE)
        page = request.GET.get('page')
        paged_products = paginator.get_page(page)
        products_count = products.count()
    context = {
        'products': paged_products,
        'products_count': products_count,
    }
    return render(request, 'store/store.html', context)


class ProductDetailsView(views.View):
    """
    Class based view for rendering the product details information page.
    """
    def get(self, *args, **kwargs):
        product_slug = self.kwargs.get('product_slug')
        category_slug = self.kwargs.get('category_slug')
        try:
            product = Product.objects.get(category__slug=category_slug, slug=product_slug)
            is_in_cart = CartItem.objects.filter(cart__cart_id=_get_cart_id(self.request), product=product).exists()
        except Exception as ex:
            raise ex

        if self.request.user.is_authenticated:
            try:
                ordered_product = OrderProduct.objects.filter(user=self.request.user, product_id=product.id).exists()
            except OrderProduct.DoesNotExist:
                ordered_product = None
        else:
            ordered_product = None

        # Get the reviews
        reviews = ReviewRating.objects.filter(product_id=product.id, status=True)

        context = {
            'product': product,
            'is_in_cart': is_in_cart,
            'ordered_product': ordered_product,
            'reviews': reviews,
        }
        return render(self.request, 'store/product_details.html', context)


class SearchView(views.ListView):
    """
    Search class based view for easy searching
    for specific keyword from the user.
    """

    model = Product
    template_name = 'store/store.html'

    def get_queryset(self):
        keyword = self.request.GET.get('keyword')
        queryset = Product.objects.all()
        if keyword:
            queryset = queryset.order_by('-created_date').filter(
                Q(description__icontains=keyword) |
                Q(product_name__icontains=keyword)
            )
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        if self.object_list:
            context['products_count'] = self.object_list.count
            context['products'] = self.object_list
            return context


def submit_review(request, product_pk):
    url = request.META.get('HTTP_REFERER')  # taking current url and save it to url variable
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_pk)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Thank you! Your review has been successfully updated.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_pk
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Thank you! Your review has been successfully submitted.')
                return redirect(url)