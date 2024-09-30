from django.utils.translation import gettext_lazy as _

CREATED = 10
PAID = 20
SHIPPED = 30
CANCELLED = 40
DELIVERED = 50

ORDER_STATUS_CHOICES = (
    (CREATED, _('Created')),
    (PAID, _('Paid')),
    (SHIPPED, _('Shipped')),
    (CANCELLED, _('Cancelled')),
    (DELIVERED, _('Delivered'))
)