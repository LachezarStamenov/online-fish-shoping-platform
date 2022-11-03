from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect

from e_fish_shop_app.cart.models import Cart, CartItem
from e_fish_shop_app.store.models import Product


def _get_cart_id(request):
    """Function to get the cart ID from session key"""
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_product_to_cart(request, product_pk):
    product = Product.objects.filter(pk=product_pk).get()
    try:
        cart = Cart.objects.filter(cart_id=_get_cart_id(request)).get()

    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_get_cart_id(request))
        cart.save()

    try:
        cart_item = CartItem.objects.filter(product=product, cart=cart).get()
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):

    try:
        cart = Cart.objects.filter(cart_id=_get_cart_id(request)).get()
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total_price) / 100
        grand_total = total_price + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)
