from base64 import urlsafe_b64decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import path
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode


User = get_user_model()

class EmailVerificationViewSet(viewsets.ViewSet):
    @action(detail=False, methods=['get'], url_path='verify_email/(?P<uidb64>[^/.]+)/(?P<token>[^/.]+)')
    def verify_email(self, request, uidb64, token):

        
        try:
            # Decoding the UID and retrieving the user
            uid = urlsafe_base64_decode(uidb64).decode()
            user = User.objects.get(pk=uid)
            
            print(user.token)
            
            # Verify the token
            if user.token == token:
                # Set the is_email_verified field to True
                user.is_email_verified = True
                user.save()

                # Return a success response
                return Response({'detail': 'Email verified successfully'})
            else:
                # Token is invalid
                return Response({'detail': 'Invalid token'}, status=400)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            # User does not exist or invalid UID
            return Response({'detail': 'Invalid user'}, status=400)
