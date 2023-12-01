from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Vehicle, LocationDetails,Booking,Booker,Passenger

User = get_user_model()

class VehicleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = '__all__'
        
class LocationDetailsSerializer(serializers.ModelSerializer):
    pick_up_date = serializers.DateField(format="%A, %d %B %Y")    
    drop_up_date = serializers.DateField(format="%A, %d %B %Y")    
    class Meta:
        model = LocationDetails
        fields = '__all__'

class LocationDetailsPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocationDetails
        fields = '__all__'

class BookingListUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password']

class PassengerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passenger
        fields = "__all__"

class BookerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booker
        fields = "__all__"

class BookingSerializer(serializers.ModelSerializer):
    user = BookingListUserSerializer()
    location_details = LocationDetailsSerializer()
    vehicle = VehicleSerializer()
    passenger = PassengerSerializer()
    booker = BookerSerializer()
    booked_on = serializers.DateField(format="%A, %d %B %Y")    

    class Meta:
        model = Booking
        fields = '__all__'

class BookingPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        exclude = ['passenger', 'booker']
