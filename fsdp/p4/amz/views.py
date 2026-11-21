from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Product

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, "accounts/login.html", {
                'error': "Invalid username or password"
            })

    return render(request, 'accounts/login.html')

@login_required(login_url='login')
def home_view(request):
    if request.method == "POST":
        name = request.POST.get("name")
        price = request.POST.get("price")
        description = request.POST.get("description")
        image_url = request.POST.get("image_url")

        Product.objects.create(
            name=name,
            price=price,
            description=description,
            image_url=image_url
        )
        return redirect('home')

    products = Product.objects.all()
    return render(request, 'accounts/home.html', {'products': products})

def register_view(request):
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            return render(request, 'accounts/register.html', {
                'error': 'Passwords do not match'
            })

        if User.objects.filter(username=email).exists():
            return render(request, 'accounts/register.html', {
                'error': 'An account with this email already exists'
            })

        user = User.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=fullname
        )
        login(request, user)
        return redirect('home')

    return render(request, 'accounts/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')