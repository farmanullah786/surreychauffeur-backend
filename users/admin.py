from django.contrib import admin
from .models import User, ForgotPasswordToken, Feedback, BillingInfo, TransferInquiry

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "username", "country", "phone", "is_active", "is_staff")
    list_filter = ("email", "username")

@admin.register(ForgotPasswordToken)
class ForgotPasswordTokenAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "token")
    list_filter = ("user__email", "token")

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "booking_order_no", "email", "location", "rating", "title", "message")
    list_filter = ("name", "booking_order_no")

@admin.register(BillingInfo)
class BillingInfoAdmin(admin.ModelAdmin):
    list_display = ("id", "billing_postcode", "billing_address", "billing_city", "billing_country")
    list_filter = ("billing_postcode", "billing_address")

@admin.register(TransferInquiry)
class TransferInquiryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "reconfirm_email", "phone_number", "num_passengers", "date", "requirements", "transfer_type")
    list_filter = ("name", "email")
