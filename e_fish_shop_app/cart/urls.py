from django.urls import path

from e_fish_shop_app.cart.views import cart

urlpatterns = (
    path('', cart, name='cart'),
)