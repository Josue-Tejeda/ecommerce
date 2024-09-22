from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from . import views

from app import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('products/', include('shop.urls', namespace='shop')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('payment/', include('payment.urls', namespace='payment')),
    path('', views.home, name='home'),
]

if settings.DEBUG:
    urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )