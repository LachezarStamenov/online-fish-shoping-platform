from django.urls import path

from e_fish_shop_app.cart.views import cart, add_product_to_cart

urlpatterns = (
    path('', cart, name='cart'),
    path('add_cart/<int:product_pk>/', add_product_to_cart, name='add product to cart'),
)
