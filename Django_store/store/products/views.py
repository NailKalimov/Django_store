from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.shortcuts import render
from products.models import Product, ProductCategory, Basket


# Create your views here.
# функции - контроллеры - вьюхи
def index(request):
    context = {'title': 'Test titile',
               'username': 'Iiiiiigor',
               'is_promotion': True}
    return render(request=request, template_name='products\index.html', context=context)


def products(request, category_id=1, page_number=1):
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, per_page=1)
    products_paginator = paginator.page(page_number)

    context = {'title': 'Store - Каталог',
               'categories': ProductCategory.objects.all(),
               'products': products_paginator}
    return render(request=request, template_name='products/products.html',
                  context=context)  # request - это экземпляр класса HTTPRequest, появляется из внутренностей Django)


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
