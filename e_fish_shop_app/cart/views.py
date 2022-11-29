from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404

from e_fish_shop_app.cart.utils import _get_cart, _get_cart_id, get_product_variation
from e_fish_shop_app.cart.models import Cart, CartItem
from e_fish_shop_app.store.models import Product
from django.views import generic as views


def add_product_to_cart(request, product_pk):
    current_user = request.user
    product = Product.objects.get(id=product_pk)

    # If the user is authenticated
    if current_user.is_authenticated:
        product_variation = get_product_variation(request, product)
        is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user).exists()

        if is_cart_item_exists:
            cart_item = CartItem.objects.filter(product=product, user=current_user)
            ex_var_list = []
            id = []

            for item in cart_item:
                existing_variation = item.variations.all()
                ex_var_list.append(list(existing_variation))
                id.append(item.id)

            if product_variation in ex_var_list:
                # increase the cart item quantity
                index = ex_var_list.index(product_variation)
                item_id = id[index]
                item = CartItem.objects.get(product=product, id=item_id)
                item.quantity += 1
                item.save()
            else:
                item = CartItem.objects.create(product=product, quantity=1, user=current_user)
                if len(product_variation) > 0:
                    item.variations.clear()
                    item.variations.add(*product_variation)
                item.save()
        else:
            cart_item = CartItem.objects.create(
                product=product,
                quantity=1,
                user=current_user,
            )
            if len(product_variation) > 0:
                cart_item.variations.clear()
                cart_item.variations.add(*product_variation)
            cart_item.save()

        return redirect('cart')

    # if the user is not authenticated
    else:
        product_variation = get_product_variation(request, product)

        try:
            cart = _get_cart(request)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_get_cart_id(request))
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


def remove_product_from_cart(request, product_pk, cart_item_pk):

    product = get_object_or_404(Product, pk=product_pk)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, pk=cart_item_pk)
        else:
            cart = _get_cart(request)
            cart_item = CartItem.objects.get(product=product, cart=cart, pk=cart_item_pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except ObjectDoesNotExist:
        raise Http404
    return redirect('cart')


class RemoveCartItemView(views.View):
    def get(self, *args, **kwargs):
        product_pk = self.kwargs.get('product_pk')
        cart_item_pk = self.kwargs.get('cart_item_pk')
        product = get_object_or_404(Product, pk=product_pk)
        if self.request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=self.request.user, pk=cart_item_pk)
        else:
            cart = _get_cart(self.request)
            cart_item = CartItem.objects.get(product=product, cart=cart, pk=cart_item_pk)
        cart_item.delete()
        return redirect('cart')


def cart(request, total_price=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = _get_cart(request)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total_price) / 100
        grand_total = total_price + tax
    except ObjectDoesNotExist:
        raise Http404
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


@login_required(login_url='login')
def checkout(request, total_price=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = _get_cart(request)
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total_price += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total_price) / 100
        grand_total = total_price + tax
    except ObjectDoesNotExist:
        raise Http404
    context = {
        'total_price': total_price,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)
