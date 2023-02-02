from django.shortcuts import render
from .models import *
from django.views.generic import DetailView
import json
import datetime
from django.http import JsonResponse
from django.http import HttpResponse
from django_daraja.mpesa.core import MpesaClient
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer=customer, complete=False)
        cartItems = order.calculate_cart_items
        
    else:
        cartItems = 0
    products = Product.objects.all()

    context = {'cartItems':cartItems,'products':products}
    return render(request, 'myapp/home.html', context)

class ProductDetailView(DetailView):
    model = Product

@login_required
def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        print(customer)
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.calculate_cart_items
        cartTotal = order.calculate_cart_total
    else:
        cartItems = 0
        order = ''
        items = ''
        cart = 0
        cartTotal = 0
 

    context={'cartTotal':cartTotal, 'order':order,'items':items, 'cartItems':cartItems}
    return render(request, 'myapp/cart.html', context)

@login_required
def updateItem(request):
    data = json.loads(request.body)

    productId = data['productId']
    action = data['action']

    print('Action', action)
    print('ProductId', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'remove-from-cart':
        orderItem.quantity = 0

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    print('Order Quantity:', orderItem.quantity)

    return JsonResponse('Item was added', safe=False)

@login_required
def payment(request):
    if request.method == 'POST':
        my_phone_number = request.POST.get('phone_number')
        print(f"This is my phone number {my_phone_number}")
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cl = MpesaClient()
        phone_number = my_phone_number
        # amount = round(order.calculate_cart_total)
        amount = 1
        account_reference = 'reference'
        transaction_desc = 'Description'
        callback_url = 'https://darajambili.herokuapp.com/express-payment';
        response = cl.stk_push(phone_number,amount, account_reference,transaction_desc,callback_url)
    else:
        response = ''
    
    context = {}
    return render(request, 'myapp/payment.html', context={})

@login_required
def stk_push_callback(request):
    data = request.body

    return HttpResponse("STK Push in Django")

@login_required
def checkout(request):
    return render(request, 'myapp/checkout.html')

@login_required
def paypal(request):
    return render(request, 'myapp/paypal.html', context ={})