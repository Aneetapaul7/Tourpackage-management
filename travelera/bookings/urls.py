from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/<int:package_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.user_dashboard, name='user_dashboard'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('vendor-bookings/', views.vendor_bookings, name='vendor_bookings'),
    path('update-status/<int:booking_id>/', views.update_booking_status, name='update_booking_status'),
]