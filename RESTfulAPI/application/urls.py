from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.home_page),
    path('api/register/', views.register_backend),
    path('api/login/', views.login_backend),
    path('api/logout/', views.logout_backend),
    path('api/list/', views.List_backend),
    path('api/view/', views.view_backend),
    path('api/average/', views.average_backend),
    path('api/rate/', views.rate_backend),
]
