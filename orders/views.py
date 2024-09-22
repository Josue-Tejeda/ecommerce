from django.shortcuts import redirect, render

from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem
from .tasks import order_created_email

def order_created(request, order_id):
    order = Order.objects.get(id=order_id)
    order_created_email.delay(order.id, request.user.email)
    return render(request, 'order/created.html', {'order': order})

def order_create(request):
    cart = Cart(request)
    if not cart:
        return redirect('home')
    
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['quantity']
                    )
            cart.clear()
            request.session['order_id'] = order.id
            return redirect('payment:process')
    else:
        form = OrderCreateForm()
    return render(request, 'order/create.html', {'cart': cart, 'form': form})
