from django.urls import path
from . import views

urlpatterns = [
    path('', views.hpg, name='home'),
    path('contact/', views.contact_view, name='contact'),  # Add this line
]

