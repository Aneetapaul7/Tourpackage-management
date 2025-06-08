from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('vendor/dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('customer/dashboard/', views.customer_dashboard, name='customer_dashboard'),
]