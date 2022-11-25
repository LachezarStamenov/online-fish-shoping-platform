from django.shortcuts import render
from django.views.generic import TemplateView

from e_fish_shop_app.store.models import Product, ReviewRating


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.all().filter(is_available=True).order_by('-created_date')
        for product in products:
            reviews = ReviewRating.objects.filter(product_id=product.id, status=True)
        context['products'] = products[:8]
        context['reviews'] = reviews

        return context
