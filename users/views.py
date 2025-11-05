import random
import matplotlib
matplotlib.use('Agg')  

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import json
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings
from django.contrib.auth import logout as auth_logout


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

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        password = request.POST.get('password','')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('distribuidor_home')   # <- NOMBRE DE RUTA, no .html
        messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/admlogin.html')  # <- render plantilla

@login_required
def distribuidor_home(request):
    user = request.user

    stats = {
        'ventas_totales': random.randint(1_000_000, 5_000_000),
        'pedidos_pendientes': random.randint(5, 25),
        'clientes_activos': random.randint(50, 150),
        'region_asignada': random.choice(['RM', 'Valparaíso', 'Biobío', 'Antofagasta']),
    }

    

    return render(request, 'users/dashboardD.html', {
        'user': user,
        'stats': stats,

    })

def genero_data(request):
    # Datos de género
    genero_data = {
        "mujeres": 80,  # Mujeres
        "hombres": 73   # Hombres
    }
    
    return JsonResponse(genero_data)

def comuna_data(request):
    # Distribución de personas por comuna
    comuna_data = [
        {"comuna": "Las Condes", "total": 61, "hombres": 30, "mujeres": 31, "malls": [
            {"mall": "Alto Las Condes", "ventas": 27},
            {"mall": "Parque Arauco", "ventas": 23},
            {"mall": "Plaza Los Dominicos", "ventas": 11}
        ]},
        {"comuna": "Ñuñoa", "total": 4, "hombres": 2, "mujeres": 2, "malls": [
            {"mall": "Plaza Egaña", "ventas": 4}
        ]},
        {"comuna": "Cerrillos", "total": 1, "hombres": 0, "mujeres": 1, "malls": [
            {"mall": "Plaza Oeste", "ventas": 1}
        ]},
        {"comuna": "Providencia", "total": 8, "hombres": 4, "mujeres": 4, "malls": [
            {"mall": "Costanera Center", "ventas": 8}
        ]},
        {"comuna": "Maipú", "total": 4, "hombres": 2, "mujeres": 2, "malls": [
            {"mall": "Arauco Maipú", "ventas": 4}
        ]},
        {"comuna": "Huechuraba", "total": 4, "hombres": 2, "mujeres": 2, "malls": [
            {"mall": "Plaza Norte", "ventas": 4}
        ]},
        {"comuna": "La Florida", "total": 3, "hombres": 1, "mujeres": 2, "malls": [
            {"mall": "Plaza Vespucio", "ventas": 2},
            {"mall": "Florida Center", "ventas": 1}
        ]}
    ]
    
    return JsonResponse(comuna_data, safe=False)

def logout_view(request):
    auth_logout(request)
    # Si el panel es sólo para distribuidores, vuelve al login de distribuidores
    return redirect('admlogin')

@login_required
def top_productos_data(request):
    # Simulado: cambia por tus queries
    data = [
        {"sku":"NK-PEG39", "nombre":"Pegasus 39", "ventas": 142},
        {"sku":"NK-AF1",   "nombre":"Air Force 1", "ventas": 131},
        {"sku":"NK-METCON","nombre":"Metcon 9",   "ventas": 97},
        {"sku":"NK-INVTN", "nombre":"Invincible 3","ventas": 76},
        {"sku":"NK-DUNK",  "nombre":"Dunk Low",    "ventas": 73},
    ]
    return JsonResponse({"labels":[d["nombre"] for d in data],
                         "values":[d["ventas"] for d in data]})

@login_required
def stock_critico_data(request):
    # Simulado: items bajo 50
    items = [
      {"sku":"NK-PEG39","producto":"Pegasus 39","tienda":"Costanera","stock":34},
      {"sku":"NK-DUNK","producto":"Dunk Low","tienda":"Alto Las Condes","stock":22},
      {"sku":"NK-METCON","producto":"Metcon 9","tienda":"Parque Arauco","stock":18},
    ]
    return JsonResponse({"rows":items})

@login_required(login_url='admlogin')
def kpi_variacion_data(request):
    """
    Devuelve el valor del mes actual, el anterior y la variación porcentual.
    Cambia esta simulación por tu query real.
    """
    actual = random.randint(800_000, 1_400_000)
    anterior = random.randint(700_000, 1_300_000)
    delta_pct = 0.0 if anterior == 0 else (actual - anterior) * 100.0 / anterior
    return JsonResponse({
        "actual": actual,
        "anterior": anterior,
        "delta_pct": delta_pct
    })


# --- Ventas por canal (donut: web/tienda/marketplace) ---
@login_required(login_url='admlogin')
def ventas_canal_data(request):
    """
    Distribución por canal para el donut.
    Ajusta los números a tu realidad o reemplaza por una query.
    """
    web = random.randint(300_000, 800_000)
    tienda = random.randint(300_000, 800_000)
    marketplace = random.randint(150_000, 500_000)
    return JsonResponse({
        "labels": ["Web", "Tienda", "Marketplace"],
        "values": [web, tienda, marketplace]
    })