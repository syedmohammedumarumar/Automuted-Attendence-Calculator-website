from django.urls import path
from attendance import views

urlpatterns = [
    path('', views.main, name='main'),
    path('home/', views.home, name='home'),
    path('calculate/', views.calculate_attendance, name='calculate_attendance'),
]
