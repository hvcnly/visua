from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='home'),
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),  
    path('login/', views.login, name='login'),
    path('hombre/', views.hombre, name='hombre'),
    path('mujer/', views.mujer, name='mujer'),
    path('infantil/', views.infantil, name='infantil'),
    path('lanzamiento/', views.lanzamiento, name='lanzamiento'),
    path('estadisticas-stock/', views.estadisticas_stock, name='estadisticas_stock'),
]
