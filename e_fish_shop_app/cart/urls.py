from django.urls import path

from e_fish_shop_app.cart.views import cart, add_product_to_cart, remove_product_from_cart, checkout, RemoveCartItemView

urlpatterns = (
    path('', cart, name='cart'),
    path('add_cart/<int:product_pk>/', add_product_to_cart, name='add product to cart'),
    path('remove_cart/<int:product_pk>/<int:cart_item_pk>/', remove_product_from_cart, name='remove product from cart'),
    path('remove_cart_item/<int:product_pk>/<int:cart_item_pk>/', RemoveCartItemView.as_view(), name='remove cart item'),

    path('checkout/', checkout, name='checkout'),
)
