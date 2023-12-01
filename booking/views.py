from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from .models import Vehicle, LocationDetails, Booker, Passenger, Booking
from .serializer import (
    VehicleSerializer,
    LocationDetailsSerializer,
    LocationDetailsPostSerializer,
    BookingPostSerializer,
    BookingSerializer
)
from custom_exceptions.exceptions import Exception404
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.http import Http404
from rest_framework import status

User = get_user_model()


@api_view(['GET', 'POST'])
@parser_classes([MultiPartParser, FormParser])
def vehicle_list(request):
    if request.method == 'GET':
        if request.GET.get("book_vehicle") and request.GET.get("uuid"):
            car_id = request.GET.get("book_vehicle")
            uuid = request.GET.get("uuid")
            if Vehicle.objects.filter(id=car_id).exists() and LocationDetails.objects.filter(id=uuid).exists():
                location_details = LocationDetails.objects.get(id=uuid)
                location_details_serializer = LocationDetailsSerializer(location_details)
                book_vehicle = Vehicle.objects.get(id=car_id)
                book_vehicle_serializer = VehicleSerializer(book_vehicle)
                data = {
                    "status_code": status.HTTP_200_OK,
                    "data": {
                        "location_details": location_details_serializer.data,
                        "book_vehicle": book_vehicle_serializer.data,
                    }
                }
                return Response(data, status=status.HTTP_200_OK)
            raise Exception404("Your Book Car Id Doesn't Exist.")

        if request.GET.get("uuid"):
            id = request.GET.get("uuid")
            if LocationDetails.objects.filter(id=id).exists():
                identifier = LocationDetails.objects.get(id=id)
                identifier_pick_up_location = identifier.identifier_pick_up_location
                location_details_serializer = LocationDetailsSerializer(identifier)
                location_details_vehicles = Vehicle.objects.filter(
                    identifier=identifier_pick_up_location, is_car_available=True
                )
                location_details_vehicles_serializer = VehicleSerializer(location_details_vehicles, many=True)
                data = {
                    "status_code": status.HTTP_200_OK,
                    "data": {
                        "location_details": location_details_serializer.data,
                        "location_vehicles": location_details_vehicles_serializer.data
                    }
                }
                return Response(data, status=status.HTTP_200_OK)
            raise Exception404("Your uuid and identifier don't exist.")

        single_cars = Vehicle.objects.filter(car_type="single")
        multiple_cars = Vehicle.objects.filter(car_type="multiple")
        cars = Vehicle.objects.all()
        single_cars = VehicleSerializer(single_cars, many=True)
        multiple_cars = VehicleSerializer(multiple_cars, many=True)
        cars = VehicleSerializer(cars, many=True)
        data = {
            "cars": cars.data,
            "single_cars": single_cars.data,
            "multiple_cars": multiple_cars.data
        }
        return Response(data)

    elif request.method == 'POST':
        serializer = VehicleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def location_details(request):
    if request.method == 'POST':
        try:
            serializer = LocationDetailsPostSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()
                data = {
                    "status_code": status.HTTP_200_OK,
                    "data": serializer.data
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'error', 'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({'status': 'error', 'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)


def booking_send_corporate_transfer_email(data, passenger, vehicle, location_details):
    reference_number = data["reference_number"]
    subject = f'Pink Berry Cars booking receipt {reference_number}'
    message = ''
    from_email = settings.EMAIL_HOST_USER
    to_email = passenger.passenger_email
    heading = ''
    html_content = f'''
        <div id=":p6" class="ii gt"
            jslog="20277; u014N:xr6bB; 1:WyIjdGhyZWFkLWY6MTc4Mzk1NTI0MjgxNDkzMjE4NCJd; 4:WyIjbXNnLWY6MTc4Mzk1NTI0MjgxNDkzMjE4NCJd">
            <!-- ... (your HTML content) ... -->
        </div>
    '''

    send_mail(subject, message, from_email, [to_email], html_message=html_content)


@api_view(['GET', 'POST', 'PUT'])
def booking(request, pk=None):
    if request.method == 'GET':
        if request.GET.get("booked_uuid"):
            uuid = request.GET.get("booked_uuid")
            booked = Booking.objects.get(id=UUID(uuid))
            serializer = BookingSerializer(booked)
            data = {
                "status_code": status.HTTP_200_OK,
                "message": "Booked Location and Ticket",
                "data": serializer.data
            }
            return Response(data)

        if pk is not None:
            user = User.objects.get(id=pk)
            booked = Booking.objects.filter(user=user.pk).order_by("-id")
            serializer = BookingSerializer(booked, many=True)
            data = {
                "status_code": status.HTTP_200_OK,
                "message": "Booking List",
                "data": serializer.data
            }
            return Response(data)

        booked = Booking.objects.all()
        serializer = BookingSerializer(booked, many=True)
        data = {
            "status_code": status.HTTP_200_OK,
            "message": "Booking List",
            "data": serializer.data
        }
        return Response(data)

    elif request.method == 'POST':
        try:
            user_id = request.data.get("user")
            if User.objects.filter(id=user_id).exists():
                user = User.objects.get(id=user_id)
                passenger = Passenger.objects.get(user=user)
                location_details_id = request.data.get("location_details")
                vehicle_id = request.data.get("vehicle")
                booked_time = request.data.get("booked_time")
                if LocationDetails.objects.filter(id=location_details_id).exists() and \
                        Vehicle.objects.filter(id=vehicle_id).exists():
                    vehicle = Vehicle.objects.get(id=vehicle_id)
                    location_details = LocationDetails.objects.get(id=location_details_id)
                    seat_number = request.data.get("seat_number")
                    data = {
                        "user": user_id,
                        "passenger": passenger.id,
                        "location_details": location_details_id,
                        "vehicle": vehicle_id,
                        "seat_number": seat_number,
                        "booked_time": booked_time,
                        "status": "pending"
                    }
                    serializer = BookingPostSerializer(data=data)
                    if serializer.is_valid():
                        serializer.save()
                        booked_data = serializer.data
                        booked_data["user"] = user.username
                        booked_data["vehicle"] = vehicle.vehicle_number
                        booked_data["location_details"] = location_details.identifier_pick_up_location
                        booked_data["seat_number"] = seat_number
                        booking_send_corporate_transfer_email(data, passenger, vehicle, location_details)
                        data = {
                            "status_code": status.HTTP_200_OK,
                            "message": "Booking Successful",
                            "data": booked_data
                        }
                        return Response(data)
                    else:
                        return Response({'status': 'error', 'message': serializer.errors},
                                        status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'status': 'error', 'message': 'Invalid location_details or vehicle ID'},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'status': 'error', 'message': 'Invalid User ID'},
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    elif request.method == 'PUT':
        if pk is not None:
            try:
                booking_data = Booking.objects.get(id=pk)
            except Booking.DoesNotExist:
                raise Http404
            serializer = BookingSerializer(booking_data, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'error', 'message': 'Invalid Booking ID'}, status=status.HTTP_400_BAD_REQUEST)
