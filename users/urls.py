from django.urls import path
from . import views

from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegisterView.as_view()),
    path('forgot-password/', views.forgot_password),
    path('reset-password/', views.reset_password),
    path('update-profile/<int:pk>', views.update_profile),
    path('billing-info/', views.BillingInfoListCreateView.as_view()),
    path('transfer-inquiry/', views.transfer_inquiry),
    path('feedbacks/', views.feedback),
]
