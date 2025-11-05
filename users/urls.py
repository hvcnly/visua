from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),
    path('estadisticas-stock/', views.estadisticas_stock, name='estadisticas_stock'),
]
