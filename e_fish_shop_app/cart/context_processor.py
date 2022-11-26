from e_fish_shop_app.cart.utils import _get_cart_id
from e_fish_shop_app.cart.models import CartItem, Cart


def cart_item_counter(request):
    cart_item_count = 0
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_get_cart_id(request))
            if request.user.is_authenticated:
                cart_items = CartItem.objects.all().filter(user=request.user)
            else:
                cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_item_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_item_count = 0
    return {'cart_item_count': cart_item_count}