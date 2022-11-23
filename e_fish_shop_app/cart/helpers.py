from e_fish_shop_app.cart.models import Cart


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
