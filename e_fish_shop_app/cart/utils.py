from e_fish_shop_app.cart.models import Cart
from e_fish_shop_app.store.models import Variation


def _get_cart_id(request):
    """Return the cart ID using the session key"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def _get_cart(request):
    """Return the cart for the given cart_id"""
    cart = Cart.objects.get(cart_id=_get_cart_id(request))
    return cart


def get_product_variation(request, product):
    """ Function which check if chosen product variation exist in the product variations"""
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key,
                                                  variation_value__iexact=value)
                product_variation.append(variation)
            except:
                pass
    return product_variation
