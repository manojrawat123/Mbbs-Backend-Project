from django.urls import path, include
from rest_framework import routers

from .views import EmailVerificationViewSet

email_verification_router = routers.DefaultRouter()
email_verification_router.register(r'email-verification', EmailVerificationViewSet, basename='email-verification')


