from django.urls import path
from . import views


urlpatterns = [
    path('shop/', views.shop, name='shop'),
    path('info/', views.info, name='info'),  
    path('login/', views.login, name='login'),
]
