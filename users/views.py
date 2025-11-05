import random
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages


# --- Vista de login para administrador (tu cambio) ---
def admin_login(request):
    """
    Vista personalizada para el login del administrador.
    Si el usuario ya está autenticado y es staff, lo redirige al panel admin.
    """
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('admin:index')
    return render(request, 'users/admlogin.html')


# --- Login normal ---
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


# --- Tienda principal ---
def shop(request):
    return render(request, 'users/shop.html')


# --- Vistas de categorías ---
def hombre(request):
    return render(request, 'users/hombre.html')

def mujer(request):
    return render(request, 'users/mujer.html')

def infantil(request):
    return render(request, 'users/infantil.html')

def lanzamiento(request):
    return render(request, 'users/lanzamiento.html')


# --- Vista de información del usuario ---
@login_required
def info(request):
    user = request.user

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


# --- Estadísticas de stock ---
@login_required
def estadisticas_stock(request):
    tiendas = [
        'Nike Costanera',
        'Nike Parque Arauco',
        'Nike Plaza Egaña',
        'Nike Mall Vivo Los Trapenses',
        'Nike Mall Florida Center'
    ]

    stocks = [random.randint(150, 400) for _ in tiendas]
    max_stock_index = stocks.index(max(stocks))

    stock_data = {
        'labels': tiendas,
        'values': stocks,
        'max_index': max_stock_index
    }

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
