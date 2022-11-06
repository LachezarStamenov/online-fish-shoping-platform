from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect, get_object_or_404

from e_fish_shop_app.cart.helpers import _get_cart
from e_fish_shop_app.cart.models import Cart, CartItem
from e_fish_shop_app.store.models import Product, Variation


def add_product_to_cart(request, product_pk):
    product = Product.objects.filter(pk=product_pk).get()
    product_variation = []  # list with all variations for the fishes(size, color)
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            try:
                variation = Variation.objects.get(
                    product=product, variation_category__iexact=key, variation_value__iexact=value
                )
                product_variation.append(variation)
            except:
                pass
    try:
        cart = _get_cart(request)
    except Cart.DoesNotExist:
        cart = _get_cart(request)
        cart.save()

    is_cart_item_exist = CartItem.objects.filter(product=product, cart=cart).exists()

    if is_cart_item_exist:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variation_lst = []
        id = []
        for item in cart_item:
            existing_variation = item.variations.all()
            existing_variation_lst.append(list(existing_variation))
            id.append(item.id)
        if product_variation in existing_variation_lst:
            index = existing_variation_lst.index(product_variation)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if len(product_variation) > 0:
                item.variations.clear()
                item.variations.add(*product_variation)
            item.save()

    else:
        cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
        if len(product_variation) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation)
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
    cart_item = CartItem.objects.get(product=product, cart=cart)
    cart_item.delete()
    return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):
    tax = 0
    grand_total = 0
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
