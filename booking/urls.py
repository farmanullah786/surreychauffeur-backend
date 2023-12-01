from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('location-details/', views.location_details),
    path('vehicles/', views.vehicle_list),
    path('booking/', views.booking),
    path('booking/<str:pk>', views.booking),
]
