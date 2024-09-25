from coupons.forms import CouponApplyForm
from django.shortcuts import render
from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages

from cart.forms import CartAddProductForm
from shop.models import Product
from .cart import Cart

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    request.session['coupon_id'] = None
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'])
        print('ITS UPDATING')
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    
    coupon_apply_form = CouponApplyForm()
    error_message = messages.get_messages(request)
    
    context = {
        'cart': cart,
        'coupon_apply_form': coupon_apply_form,
        'error_message': error_message
    }
    return render(request, 'cart/detail.html', context)