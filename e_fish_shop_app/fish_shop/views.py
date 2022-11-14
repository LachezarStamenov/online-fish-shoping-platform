from django.shortcuts import render
from django.views.generic import TemplateView

from e_fish_shop_app.store.models import Product


# def home(request):
#     products = Product.objects.all().filter(is_available=True)
#     context = {
#         'products': products,
#     }
#     return render(request, 'index.html', context)

class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['products'] = Product.objects.all().filter(is_available=True)
        return context
