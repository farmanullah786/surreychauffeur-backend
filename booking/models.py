from django.db import models
from users.models import User
import uuid

class Vehicle(models.Model):
    CAR_TYPE_CHOICES = [
        ('single', 'Single'),
        ('multiple', 'Multiple'),
    ]
    
    name = models.CharField(max_length=255, verbose_name="Name")
    passenger_capacity = models.IntegerField(verbose_name="Passenger Capacity")
    check_in_luggage_capacity = models.IntegerField(verbose_name="Check-in Luggage Capacity")
    hand_luggage_capacity = models.IntegerField(verbose_name="Hand Luggage Capacity")
    image = models.ImageField(upload_to='vehicle_images/', verbose_name="Image")
    car_type = models.CharField(max_length=9, choices=CAR_TYPE_CHOICES, verbose_name="Car Type")
    is_car_available = models.BooleanField(default=True, verbose_name="Is Car Available")
    identifier = models.CharField(max_length=255, verbose_name="Identifier")
    price_per_km = models.IntegerField(verbose_name="Price per Kilometer")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Vehicles"

class LocationDetails(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    pick_up_location = models.CharField(max_length=255, verbose_name="Pick-up Location")
    identifier_pick_up_location = models.CharField(max_length=255, verbose_name="Identifier (Pick-up)")
    label_pick_up_location = models.CharField(max_length=255, verbose_name="Label (Pick-up)")
    type_of_pick_up_location = models.CharField(max_length=255, verbose_name="Type of Location (Pick-up)")
    drop_up_location = models.CharField(max_length=255, verbose_name="Drop-off Location")
    identifier_drop_up_location = models.CharField(max_length=255, verbose_name="Identifier (Drop-off)")
    label_drop_up_location = models.CharField(max_length=255, verbose_name="Label (Drop-off)")
    type_of_drop_up_location = models.CharField(max_length=255, verbose_name="Type of Location (Drop-off)")
    pick_up_date = models.DateField(verbose_name="Pick-up Date")
    drop_up_date = models.DateField(null=True, blank=True, verbose_name="Drop-off Date")
    one_way = models.BooleanField(default=False, verbose_name="One Way")
    two_way = models.BooleanField(default=False, null=True, blank=True, verbose_name="Two Way")
    vias = models.JSONField(default=list, null=True, blank=True, verbose_name="Vias")

    def __str__(self):
        return f"Location Details - {self.pick_up_location} to {self.drop_up_location}"

    class Meta:
        verbose_name_plural = "Location Details"

class Booker(models.Model):
    booker_full_name = models.CharField(max_length=255, verbose_name="Full Name")
    booker_email = models.EmailField(verbose_name="Email")
    booker_mobile_country_code = models.CharField(max_length=255, verbose_name="Mobile Country Code")
    booker_mobile_number = models.CharField(max_length=40, verbose_name="Mobile Number")
    booker_home_country_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Home Country Code")
    booker_home_number = models.CharField(max_length=40, blank=True, null=True, verbose_name="Home Number")

    def __str__(self):
        return self.booker_full_name

    class Meta:
        verbose_name_plural = "Bookers"

class Passenger(models.Model):
    passenger_first_name = models.CharField(max_length=255, verbose_name="First Name")
    passenger_last_name = models.CharField(max_length=255, verbose_name="Last Name")
    passenger_email = models.EmailField(blank=True, null=True, verbose_name="Email")
    passenger_mobile_country_code = models.CharField(max_length=255, verbose_name="Mobile Country Code")
    passenger_mobile_number = models.CharField(max_length=40, verbose_name="Mobile Number")
    passenger_home_country_code = models.CharField(max_length=255, blank=True, null=True, verbose_name="Home Country Code")
    passenger_home_number = models.CharField(max_length=40, blank=True, null=True, verbose_name="Home Number")

    def __str__(self):
        return f"{self.passenger_first_name} {self.passenger_last_name}"

    class Meta:
        verbose_name_plural = "Passengers"

class Booking(models.Model):
    BOOKING_STATUS = [
        ('Paid', 'Paid'),
        ('Cancelled', 'Cancelled'),
        ('Unpaid', 'Unpaid'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name="ID")
    location_details = models.ForeignKey(LocationDetails, on_delete=models.CASCADE, related_name="location_details", verbose_name="Location Details")
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name="vehicle", verbose_name="Vehicle")
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="user", verbose_name="User")
    booker = models.ForeignKey(Booker, on_delete=models.SET_NULL, null=True, blank=True, related_name="booker", verbose_name="Booker")
    passenger = models.ForeignKey(Passenger, on_delete=models.SET_NULL, null=True, blank=True, related_name="passenger", verbose_name="Passenger")
    flight_number = models.CharField(max_length=10, verbose_name="Flight Number")
    coming_from = models.CharField(max_length=255, verbose_name="Coming From")
    hours = models.CharField(max_length=255, verbose_name="Hours")
    return_hours = models.CharField(max_length=255, blank=True, null=True, verbose_name="Return Hours")
    minutes = models.CharField(max_length=255, verbose_name="Minutes")
    return_minutes = models.CharField(max_length=255, blank=True, null=True, verbose_name="Return Minutes")
    waiting_time = models.IntegerField(verbose_name="Waiting Time")
    return_waiting_time = models.IntegerField(blank=True, null=True, verbose_name="Return Waiting Time")
    return_flight_number = models.CharField(max_length=10, blank=True, null=True, verbose_name="Return Flight Number")
    is_passenger = models.CharField(max_length=255, verbose_name="Is Passenger")
    passenger_capacity = models.CharField(max_length=255, blank=True, null=True, verbose_name="Passenger Capacity")
    check_in_luggage_capacity = models.CharField(max_length=255, blank=True, null=True, verbose_name="Check-in Luggage Capacity")
    hand_luggage_capacity = models.CharField(max_length=255, blank=True, null=True, verbose_name="Hand Luggage Capacity")
    first_child_seat_required = models.CharField(max_length=255, blank=True, null=True, verbose_name="First Child Seat Required")
    second_child_seat_required = models.CharField(max_length=255, blank=True, null=True, verbose_name="Second Child Seat Required")
    price = models.IntegerField(verbose_name="Price")
    special_requirements = models.TextField(blank=True, null=True, verbose_name="Special Requirements")
    reference_number = models.CharField(max_length=255, verbose_name="Reference Number")
    return_reference_number = models.CharField(max_length=255, blank=True, null=True, verbose_name="Return Reference Number")
    payment_type = models.CharField(max_length=255, verbose_name="Payment Type")
    booked_on = models.DateField(auto_now=True, verbose_name="Booked On")
    status = models.CharField(max_length=22, choices=BOOKING_STATUS, default="Unpaid", verbose_name="Status")

    class Meta:
        verbose_name_plural = "Bookings"
