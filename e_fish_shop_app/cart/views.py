from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from e_fish_shop_app.cart.helpers import _get_cart_id, _get_cart
from e_fish_shop_app.cart.models import Cart, CartItem
from e_fish_shop_app.store.models import Product


def add_product_to_cart(request, product_pk):
    product = Product.objects.filter(pk=product_pk).get()
    try:
        cart = _get_cart(request)
    except Cart.DoesNotExist:
        cart = _get_cart(request)
        cart.save()

    try:
        cart_item = CartItem.objects.filter(product=product, cart=cart).get()
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        cart_item.save()

    return redirect('cart')


def remove_product_from_cart(request, product_pk):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    cart_item = CartItem.objects.filter(product=product, cart=cart).get()
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


def remove_cart_item(request, product_pk):
    cart = _get_cart(request)
    product = get_object_or_404(Product, pk=product_pk)
    cart_item = CartItem.objects.filter(product=product, cart=cart).get()
    cart_item.delete()
    return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        cart = _get_cart(request)
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
