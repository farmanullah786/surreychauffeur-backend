from django.db.models import Avg
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.hashers import make_password

from rest_framework import status, generics
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializer import (
    MyTokenObtainPairSerializer,
    RegisterSerializer,
    FeedbackSerializer,
    ForgotPasswordSerializer,
    UserProfileSerializer,
    BillingInfoSerializer,
    TransferInquirySerializer,
)

from custom_exceptions.exceptions import Exception404

from .models import Feedback, ForgotPasswordToken, BillingInfo
from django.contrib.auth import get_user_model

User = get_user_model()
import jwt


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        # Extract only the access token from the response
        access_token = response.data.get('access')
        return Response({'access_token': access_token})

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class BillingInfoListCreateView(generics.ListCreateAPIView):
    queryset = BillingInfo.objects.all()
    serializer_class = BillingInfoSerializer

@api_view(['POST'])
def forgot_password(request):
    if request.method == 'POST':
        email = request.data.get('email')
        serializer = ForgotPasswordSerializer(data=request.data)

        if serializer.is_valid():
            user = User.objects.get(email=email)

            existing_token = ForgotPasswordToken.objects.filter(user=user).first()
            token_data = {
                'user_id': user.id,
                'email': user.email,
            }
            secret_key = settings.SECRET_KEY
            token = jwt.encode(token_data, secret_key, algorithm='HS256').decode('utf-8')

            if existing_token:
                # Use existing token if available
                existing_token.token = token
                existing_token.save()
            else:
                existing_token = ForgotPasswordToken.objects.create(user=user, token=token)

            # Send email with the token
            subject = 'Password Reset'
            message = f'Dear {user.first_name + " " + user.last_name} \nPlease copy and paste the link below into your browser to change your password. \n:{"http://localhost:3000/reset-password?token=" + token} \n*This is an automated email*'
            to_email = user.email
            send_mail(subject, message, settings.EMAIL_HOST_USER, [to_email], fail_silently=False)

            data = {
                "status_code": status.HTTP_200_OK,
                "message": "Please enter your new password.",
                "data": existing_token.token
            }

            return Response(data, status=status.HTTP_200_OK)

        return Response({"error": "Invalid data provided.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def reset_password(request):
    if request.method == 'POST':
        user_token = request.data.get('user_token')
        logged_user_email = request.data.get('logged_user')

        if user_token:
            # Reset password for a user with a token
            if ForgotPasswordToken.objects.filter(token=user_token).exists():
                forgot_password_token = ForgotPasswordToken.objects.get(token=user_token)
                user = forgot_password_token.user
                password = request.data['password']

                user.password = make_password(password)
                user.save()
                forgot_password_token.delete()

                # Send email notification
                subject = 'Password Changed'
                message = f'Dear {user.full_name()} \nYou have changed your password, and your new login details are below. \nUser Name: {user.email} \nPassword: {password}\n*This is an automated email*'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)

                data = {
                    "status_code": status.HTTP_200_OK,
                    "message": "Your password has been successfully changed.",
                }
                return Response(data, status=status.HTTP_200_OK)

        elif logged_user_email:
            # Reset password for a logged-in user
            if User.objects.filter(email=logged_user_email).exists():
                logged_user = User.objects.get(email=logged_user_email)
                password = request.data['password']

                logged_user.password = make_password(password)
                logged_user.save()

                # Send email notification
                subject = 'Password Changed'
                message = f'Dear {logged_user.full_name()} \nYou have changed your password, and your new login details are below. \nUser Name: {logged_user.email} \nPassword: {password}\n*This is an automated email*'
                send_mail(subject, message, settings.EMAIL_HOST_USER, [logged_user.email], fail_silently=False)

                data = {
                    "status_code": status.HTTP_200_OK,
                    "message": "Your password has been successfully changed.",
                }
                return Response(data, status=status.HTTP_200_OK)

        else:
            raise Exception404("Your token is invalid or time has expired")

    return Response({"error": "Invalid data provided."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request, pk=None):
    if request.method == 'GET':
        try:
            user_profile = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile)
            data = {
                "status_code": 200,
                "message": "Login User",
                "data": serializer.data,
            }
            return Response(data)
        except User.DoesNotExist:
            raise Exception404(f"User not exist with id: {pk}")

    if request.method == 'PUT':
        try:
            user_profile = User.objects.get(pk=pk)
            serializer = UserProfileSerializer(user_profile, data=request.data)
            if serializer.is_valid():
                serializer.save()
                data = {
                    "status_code": 200,
                    "message": "Profile successfully updated!",
                    "data": serializer.data,
                }
                return Response(data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            raise Exception404(f"User not exist with id: {pk}")
        
@api_view(['GET', 'POST'])
def feedback(request):
    if request.method == 'GET':
        feedback_list = Feedback.objects.all()
        average_rating = Feedback.objects.aggregate(Avg('rating'))['rating__avg']
        serializer = FeedbackSerializer(feedback_list, many=True)

        data = {
            "status_code": status.HTTP_200_OK,
            "message": "Feedback List",
            "data": {
                "feedback_list": serializer.data,
                "average_rating": average_rating if average_rating else 0,
                "reviews": len(feedback_list),
            }
        }
        
        return Response(data)

    elif request.method == 'POST':
        serializer = FeedbackSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            data = {
                "status_code": status.HTTP_201_CREATED,
                "message": "Feedback submitted successfully.",
                "data": serializer.data,
            }
            
            return Response(data, status=status.HTTP_201_CREATED)

        return Response({"error": "Feedback not submitted.", "details": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

def send_corporate_transfer_email(data):
    transfer_type = data['transfer_type'].capitalize()
    subject = f'{transfer_type} Transfer Inquiry'
    message = 'Thank you for submitting your inquiry.'
    from_email = settings.EMAIL_HOST_USER
    to_email = data['email']

    html_content = f'''
        <table border="1" cellspacing="0" cellpadding="0" style="
            border-collapse: collapse;
            border: #d4e0ee 1px solid;
            background-color: White;
            font-family: verdana, arial;
            font-size: 11px;
            font-weight: normal;
            color: #000;
            text-decoration: none;
            width: 100%;
        ">
            <tbody>
                <tr>
                    <td colspan="2" style="
                        padding: 10px;
                        font-weight: bold;
                        border: #d4e0ee 1px solid;
                    ">
                        <h3 style="
                            font-size: 17px;
                            font-weight: bold;
                            background-color: #3e014f;
                            color: white;
                            margin: 0;
                            padding: 8px 15px;
                        ">{transfer_type} Transfer Inquiry</h3>
                    </td>
                </tr>
                <!-- More rows for different pieces of information -->
                <tr>
                    <td colspan="2" style="
                        padding: 10px;
                        color: #ff2c94;
                        font-weight: normal;
                    ">
                        Copyright © <a href="http://pinkberrycars.com" target="_blank"
                            style="color: #ff2c94; text-decoration: none;"
                            >pinkberrycars.com</a> All rights reserved.
                    </td>
                </tr>
            </tbody>
        </table>
    '''

    send_mail(subject, message, from_email, [to_email], html_message=html_content)

@api_view(['POST'])
def transfer_inquiry(request):
    if request.method == 'POST':
        serializer = TransferInquirySerializer(data=request.data)
        transfer_type = request.data['transfer_type'].capitalize()
        transfer_message = f'{transfer_type} Inquiry Created'

        if serializer.is_valid():
            serializer.save()
            send_corporate_transfer_email(serializer.data)

            data = {
                "status_code": 200,
                "message": transfer_message,
                "data": serializer.data,
            }

            return Response(data)

        return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)



