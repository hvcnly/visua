from django.shortcuts import render

def shop(request):
    return render(request, 'users/shop.html')

def login(request):
    return render(request, 'users/login.html')
