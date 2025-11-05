import io
import base64
import random
import matplotlib
matplotlib.use('Agg')  
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.http import JsonResponse
from django.utils.timezone import now
from django.conf import settings
import csv, traceback

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('info')  # redirige a /users/info
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')

    return render(request, 'users/login.html')



def shop(request):
    return render(request, 'users/shop.html')

@login_required
def info(request):
    user = request.user

    stats = {
        'total_pedidos': random.randint(5, 20),
        'productos_favoritos': random.randint(5, 30),
        'nivel_membresia': random.choice(['Bronze', 'Silver', 'Gold', 'Platinum']),
        'tiendas_top': [
            {'nombre': 'Nike Costanera', 'stock': random.randint(150, 400)},
            {'nombre': 'Nike Parque Arauco', 'stock': random.randint(150, 400)},
            {'nombre': 'Nike Plaza Egaña', 'stock': random.randint(150, 400)},
            {'nombre': 'Nike Mall Vivo Los Trapenses', 'stock': random.randint(150, 400)},
            {'nombre': 'Nike Mall Florida Center', 'stock': random.randint(150, 400)},
        ]
    }

    tiendas = stats['tiendas_top']
    nombres = [t['nombre'] for t in tiendas]
    stocks = [t['stock'] for t in tiendas]
    x = [random.uniform(-70.7, -70.5) for _ in tiendas]  
    y = [random.uniform(-33.6, -33.3) for _ in tiendas] 

    plt.figure(figsize=(6, 5))
    plt.scatter(x, y, s=[s*0.3 for s in stocks], c='red', alpha=0.6)
    for i, nombre in enumerate(nombres):
        plt.text(x[i]+0.005, y[i]+0.005, nombre, fontsize=8)
    plt.title("🗺️ Tiendas Nike Santiago - Stock simulado", fontsize=12)
    plt.xlabel("Longitud")
    plt.ylabel("Latitud")
    plt.grid(True, linestyle='--', alpha=0.3)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight')
    buffer.seek(0)
    mapa_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    plt.figure(figsize=(6, 3))
    plt.bar(nombres, stocks, color='black')
    plt.title("Stock total por tienda", fontsize=12)
    plt.xticks(rotation=30, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.3)

    buffer2 = io.BytesIO()
    plt.savefig(buffer2, format='png', bbox_inches='tight')
    buffer2.seek(0)
    grafico_stock = base64.b64encode(buffer2.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'users/info.html', {
        'user': user,
        'stats': stats,
        'mapa': mapa_base64,
        'grafico_stock': grafico_stock,
    })
def distribuidor_login(request):
    # MISMO flujo que el login normal, pero con su propio template
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # (Opcional) verificar grupo "Distribuidores"
            # if not user.groups.filter(name='Distribuidores').exists():
            #     messages.error(request, 'No tienes permiso de distribuidor.')
            #     return redirect('login')
            auth_login(request, user)
            return redirect('distribuidor_home')  # o a una vista específica: 'distribuidor_home'
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    return render(request, 'users/distribuidor.html')  # <- ruta correcta


@login_required
def distribuidor_home(request):
    user = request.user

    stats = {
        'ventas_totales': random.randint(1_000_000, 5_000_000),
        'pedidos_pendientes': random.randint(5, 25),
        'clientes_activos': random.randint(50, 150),
        'region_asignada': random.choice(['RM', 'Valparaíso', 'Biobío', 'Antofagasta']),
    }

    meses = ['Jul', 'Ago', 'Sep', 'Oct', 'Nov']
    ventas = [random.randint(500000, 1200000) for _ in meses]

    plt.figure(figsize=(6, 3))
    plt.plot(meses, ventas, marker='o', color='#f5f5f5')
    plt.title('Ventas mensuales simuladas', color='white')
    plt.xlabel('Mes', color='white')
    plt.ylabel('Ventas (CLP)', color='white')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().set_facecolor('#111')
    plt.gcf().patch.set_facecolor('#111')
    plt.tick_params(colors='white')

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', facecolor='#111')
    buffer.seek(0)
    grafico_ventas = base64.b64encode(buffer.getvalue()).decode('utf-8')
    plt.close()

    return render(request, 'users/dashboardD.html', {
        'user': user,
        'stats': stats,
        'grafico_ventas': grafico_ventas,
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
