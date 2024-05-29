from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Category, Cart, CartItem, Order, OrderItem
from .forms import CartForm
from django.db import transaction
#ku display items zenye ziko kwa database kwa html files

def category_list(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})


def product_list(request, category_id=None):
    categories = Category.objects.all()
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    return render(request, 'category_list.html', {'products': products, 'categories': categories})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'category_list.html', {'product': product})


@login_required
def add_to_cart(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = CartForm(request.POST)
        if form.is_valid():
            cart, created = Cart.objects.get_or_create(user=request.user)
            quantity = form.cleaned_data['quantity']
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            return redirect('cart')
    else:
        form = CartForm()
    return render(request, 'add_to_cart.html', {'form': form})


def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')

    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        total_price = sum(item.product.price * item.quantity for item in cart_items)
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    return render(request, 'view_cart.html', {'cart_items': cart_items, 'total_price': total_price})


@login_required
def remove_from_cart(request, pk):
    cart_item = get_object_or_404(CartItem, pk=pk)
    cart_item.delete()
    return redirect('cart')


@login_required
def checkout(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        if not cart_items.exists():
            return redirect('view_cart')

        total_price = sum(item.product.price * item.quantity for item in cart_items)

        with transaction.atomic():
            order = Order.objects.create(user=request.user, total_price=total_price)

            for item in cart_items:
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)
                item.delete()

        return render(request, 'checkout_success.html', {'order': order})
    except Cart.DoesNotExist:
        return redirect('view_cart')





@login_required
def order_confirmation(request):
    return render(request, 'order_confirmation.html')





from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')

