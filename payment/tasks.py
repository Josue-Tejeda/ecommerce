from io import BytesIO
import weasyprint
from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from app.settings import FROM_EMAIL
from orders.models import Order

@shared_task
def payment_completed(order_id):
    order = Order.objects.get(id=order_id)
    subject = f'Ecommerce - Invoice no. {order.id}'
    message = 'Please, find attached the invoice for your recent purchase.'
    email = EmailMessage(
        subject,
        message,
        FROM_EMAIL,
        [order.email]
    )
    html = render_to_string('admin/order/order_invoice.html', {'order': order})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)
    email.attach(f'order_{order.id}.pdf', out.getvalue(), 'application/pdf')
    email.send()
    