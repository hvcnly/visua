import random
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('info')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'users/login.html')

def shop(request):
    return render(request, 'users/shop.html')

def hombre(request):
    return render(request, 'users/hombre.html')

def mujer(request):
    return render(request, 'users/mujer.html')

def infantil(request):
    return render(request, 'users/infantil.html')

def lanzamiento(request):
    return render(request, 'users/lanzamiento.html')

@login_required
def info(request):
    user = request.user

    # Datos para el historial de compras
    historial_compras = [
        {'producto': 'Air Jordan 1 Retro High', 'fecha': '15/10/2024', 'estado': 'Entregado', 'precio': 149990},
        {'producto': 'Nike Sportswear Hoodie', 'fecha': '02/10/2024', 'estado': 'Entregado', 'precio': 49990},
        {'producto': 'Nike Dri-FIT Running', 'fecha': '25/09/2024', 'estado': 'Entregado', 'precio': 29990},
        {'producto': 'Jordan Series ES', 'fecha': '18/09/2024', 'estado': 'Entregado', 'precio': 89990},
    ]

    stats = {
        'productos_favoritos': random.randint(5, 30),
        'nivel_membresia': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
        'historial_compras': historial_compras,
        'total_compras': len(historial_compras),
        'gasto_total': sum(compra['precio'] for compra in historial_compras)
    }

    return render(request, 'users/info.html', {
        'user': user,
        'stats': stats,
    })

@login_required
def estadisticas_stock(request):
    # Datos para el gráfico de distribución de stock (Doughnut)
    tiendas = [
        'Nike Costanera', 
        'Nike Parque Arauco', 
        'Nike Plaza Egaña', 
        'Nike Mall Vivo Los Trapenses', 
        'Nike Mall Florida Center'
    ]
    
    # Generar stocks y encontrar el máximo
    stocks = [random.randint(150, 400) for _ in tiendas]
    max_stock_index = stocks.index(max(stocks))
    
    stock_data = {
        'labels': tiendas,
        'values': stocks,
        'max_index': max_stock_index
    }
    
    # Datos para el gráfico de top tiendas (Barras)
    visitas = [random.randint(500, 2000) for _ in tiendas]
    max_visitas_index = visitas.index(max(visitas))
    
    top_stores_data = {
        'labels': tiendas,
        'visitas': visitas,
        'max_index': max_visitas_index
    }

    return render(request, 'users/estadisticas_stock.html', {
        'user': request.user,
        'stock_data': json.dumps(stock_data),
        'top_stores_data': json.dumps(top_stores_data),
    })