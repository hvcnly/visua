import io
import base64
import random
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('/users/info/') 
        else:
            error = "Usuario o contraseña incorrectos"
            return render(request, 'users/login.html', {'error': error})
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
