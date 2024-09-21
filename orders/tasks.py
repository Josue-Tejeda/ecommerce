from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import Order

@shared_task
def order_created_email(order_id, user_email):
    """
    Task to send an email notification when an order is successfully created.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order Confirmation - Order #{order.id}'
    
    html_message = render_to_string('order_created_email.html', {'order': order})
    plain_message = strip_tags(html_message)

    mail_sent = send_mail(
        subject,
        plain_message,
        'admin@app.com',
        [user_email],
        html_message=html_message
    )
    
    return mail_sent
