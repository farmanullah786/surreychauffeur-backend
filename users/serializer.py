from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from custom_exceptions.exceptions import Exception409
from .models import TransferInquiry, Feedback, BillingInfo

User = get_user_model()



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims to the JWT token payload
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['country'] = user.country
        token['email'] = user.email
        token['phone'] = user.phone
        token['full_name'] = user.full_name()
        return token


class RegisterSerializer(serializers.ModelSerializer):
    # Serializer for user registration
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = (
            'email',
            'password',
            'password2',
            'first_name',
            'last_name',
            'country',
            'phone',
        )

    def validate_email(self, value):
        # Custom validation to check if the email is already in use
        if User.objects.filter(email=value).exists():
            raise Exception409("This email address is already in use.")
        return value

    def validate(self, attrs):
        # Custom validation to ensure password and password2 match
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        # Create and save the new user instance
        user = User.objects.create(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            country=validated_data['country'],
            phone=validated_data['phone'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class ForgotPasswordSerializer(serializers.Serializer):
    # Serializer for handling forgotten password requests
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ('email',)

    def validate_email(self, value):
        # Custom validation to check if the user with the provided email exists
        try:
            user = User.objects.get(email=value)
        except User.DoesNotExist:
            raise Exception409("User with this email does not exist.")
        return value

class TransferInquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = TransferInquiry
        fields = '__all__'


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['name', 'LocationDetails_order_no', 'email', 'location', 'rating', 'title', 'message']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'country', 'phone']


class BillingInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillingInfo
        fields = '__all__'