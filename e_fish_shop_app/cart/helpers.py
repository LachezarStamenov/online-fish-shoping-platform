from e_fish_shop_app.cart.models import Cart


def _get_cart_id(request):
    """Function which return the cart ID from session key"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def _get_cart(request):
    """Function which return the cart for the given cart_id"""
    cart = Cart.objects.filter(cart_id=_get_cart_id(request)).get()
    return cart
