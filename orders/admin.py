import csv, datetime
from django.http import HttpResponse
from django.urls import reverse
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    
    
def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename={opts.verbose_name}_report.csv'
    writer = csv.writer(response)
    
    fields = [field for field in opts.get_fields() if not field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name.upper() for field in fields])
    
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response

def order_detail(obj):
    url = reverse('orders:admin_order_detail', args=[obj.id])
    return mark_safe(f'<a href="{url}">View</a>')

def order_payment(obj):
    url = obj.get_stripe_url()
    if obj.stripe_id:
        html = f'<a href="{url}" target="_blank">{obj.stripe_id}</a>'
        return mark_safe(html)
    return '-'

def order_pdf(obj):
    url = reverse('orders:admin_order_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}">PDF</a>')

order_payment.short_description = 'Stripe ID'
export_to_csv.short_description = 'Export to CSV'
order_pdf.short_description = 'Invoice'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id',
                    'status',
                    'first_name',
                    'last_name',
                    'email',
                    'phone',
                    'address',
                    'city',
                    'created_at',
                    'updated_at',
                    order_pdf,
                    order_detail,
                    order_payment]
    list_filter = ['status', 'created_at', 'updated_at']
    inlines = [OrderItemInline]
    actions = [export_to_csv]
    
