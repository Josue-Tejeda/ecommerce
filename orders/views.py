import weasyprint
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.admin.views.decorators import staff_member_required
from django.template.loader import render_to_string

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


@staff_member_required
def admin_order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    return render(request, 'admin/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    order = Order.objects.get(id=order_id)
    html = render_to_string('admin/order/order_invoice.html', {'order': order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="order_{order.id}.pdf"'
    
    weasyprint.HTML(string=html).write_pdf(response,)
    
    return response

    