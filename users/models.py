from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .managers import CustomUserManager

class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True, verbose_name="Email")
    username = models.CharField(max_length=30, unique=True, blank=True, null=True, verbose_name="Username")

    # Add other fields as needed
    country = models.CharField(max_length=255, blank=True, null=True, verbose_name="Country")
    phone = models.IntegerField(blank=True, null=True, verbose_name="Phone")

    is_active = models.BooleanField(default=True, verbose_name="Active")
    is_staff = models.BooleanField(default=False, verbose_name="Staff")

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Add other required fields here

    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Users"


class ForgotPasswordToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User")
    token = models.CharField(max_length=255, verbose_name="Token")

    def __str__(self):
        return f"Token: {self.token}"

    class Meta:
        verbose_name_plural = "Forgot Password Tokens"


class Feedback(models.Model):
    name = models.CharField(max_length=255, verbose_name="Name")
    booking_order_no = models.CharField(max_length=255, verbose_name="Booking Order No")
    email = models.EmailField(verbose_name="Email")
    location = models.CharField(max_length=255, verbose_name="Location")
    rating = models.PositiveIntegerField(verbose_name="Rating")
    title = models.CharField(max_length=255, verbose_name="Title")
    message = models.TextField(verbose_name="Message")

    def __str__(self):
        return f"{self.name} - {self.title}"

    class Meta:
        verbose_name_plural = "Feedback"


class BillingInfo(models.Model):
    billing_postcode = models.CharField(max_length=10, verbose_name="Billing Postcode")
    billing_address = models.CharField(max_length=100, verbose_name="Billing Address")
    billing_city = models.CharField(max_length=100, verbose_name="Billing City")
    billing_country = models.CharField(max_length=100, verbose_name="Billing Country")

    def __str__(self):
        return self.billing_postcode

    class Meta:
        verbose_name_plural = "Billing Information"


class TransferInquiry(models.Model):
    TRANSFER_TYPE_CHOICES = [
        ('group', 'Group Transfer'),
        ('corporate', 'Corporate Transfer'),
        ('sightseeing', 'Sightseeing Transfer'),
    ]

    name = models.CharField(max_length=255, verbose_name="Name")
    email = models.EmailField(verbose_name="Email")
    reconfirm_email = models.EmailField(verbose_name="Reconfirm Email")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    num_passengers = models.IntegerField(null=True, blank=True, verbose_name="Number of Passengers")
    date = models.DateField(null=True, blank=True, verbose_name="Date")
    requirements = models.TextField(verbose_name="Requirements")
    transfer_type = models.CharField(max_length=12, choices=TRANSFER_TYPE_CHOICES, verbose_name="Transfer Type")

    def __str__(self):
        return f'{self.name} - {self.transfer_type}'

    class Meta:
        verbose_name_plural = "Transfer Inquiries"
