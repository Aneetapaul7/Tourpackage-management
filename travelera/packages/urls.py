from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('create/', views.create_package, name='create_package'),
    path('vendor-dashboard/', views.vendor_dashboard, name='vendor_dashboard'),
    path('edit/<int:pk>/', views.edit_package, name='edit_package'),
    path('delete/<int:pk>/', views.delete_package, name='delete_package'),
    path('bookings/<int:package_id>/', views.vendor_bookings, name='vendor_bookings'),
    path('', views.package_list, name='package_list'),
    path('<int:pk>/', views.package_detail, name='package_detail'),
    path('book/<int:package_id>/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.user_dashboard, name='user_dashboard'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('logout/', views.logout, name='logout'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)