from django.contrib import admin
from .models import  LocationDetails, Vehicle, Booking

@admin.register(LocationDetails)
class LocationDetailsAdmin(admin.ModelAdmin):
    list_display = ("id",)
    list_filter = ()  # Add filters as needed

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    list_filter = ("id", "name")  # Add filters as needed

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id",)
    list_filter = ()  # Add filters as needed
