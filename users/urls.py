from django.urls import path
from . import views


urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),  
    path('login/', views.login, name='login'),
    path('distribuidor/', views.distribuidor_login, name='distribuidor_login'),
    path('distribuidor/home/', views.distribuidor_home, name='distribuidor_home'),
    path('genero_data/', views.genero_data, name='genero_data'),
    path('comuna_data/', views.comuna_data, name='comuna_data'),
    path('api/stock-critico/', views.stock_critico_data, name='stock_critico_data'),
    path('api/top-productos/', views.top_productos_data, name='top_productos_data'),
]

