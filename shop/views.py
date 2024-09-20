from django.shortcuts import get_object_or_404, render

from shop.models import Category, Product
from cart.forms import CartAddProductForm

def product_list(request, category_slug=None):
    template = 'shop/product/list.html'
    category = None
    categories = Category.objects.all()
    products = Product.objects.get_all_available()
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
        
    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
        
    return render(request, template, context)


def product_detail(request, id, slug):
    template = 'shop/product/detail.html'
    product = get_object_or_404(Product, id=id, slug=slug, is_available=True)
    cart_product_form = CartAddProductForm()
    context = {
        'product': product,
        'cart_product_form': cart_product_form
    }
    
    return render(request, template, context)