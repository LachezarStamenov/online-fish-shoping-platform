from django.shortcuts import render
from django.views import generic as views
from e_fish_shop_app.store.models import Product


class StoreView(views.TemplateView):
    template_name = 'store/store.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().filter(is_available=True)
        context['products_count'] = len(Product.objects.all().filter(is_available=True))
        return context
