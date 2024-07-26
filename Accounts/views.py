from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import AccountSerializer,UserSerializer,UserProfileSerializer
from .models import Account, User, UserProfile
from rest_framework import status
from rest_framework.response import Response


class AccountViewSet(ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    authentication_classes = [JWTAuthentication]  

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action in ['retrieve', 'update']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                print('Admin', self.request.user)
                return self.queryset.all()
            else:
                print('Normal User', self.request.user)
                return self.queryset.filter(user=self.request.user)
        else:
            print('Anonymous User')
            return self.queryset.none()

    def create(self, request, *args, **kwargs):
        # print(request.text)
        print(request.data)
        print(request.headers)
        # print(request.json())
        return super().create(request, *args, **kwargs)  
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        
        serializer.is_valid(raise_exception=True)
        # Additional check to ensure the user can only update their own account
        if not request.user.is_admin and instance.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)
        
        self.perform_update(serializer)
        
        return Response(serializer.data)
    
    
    
        
        
        


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]  

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                print('Admin', self.request.user)
                return self.queryset.all()
            else:
                print('Normal User', self.request.user,self.request.user.get_username())
                return self.queryset.filter(email=self.request.user.get_username())
        else:
            print('Anonymous User')
            return self.queryset.none()

class UserProfileViewSet(ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    authentication_classes = [JWTAuthentication]  

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [AllowAny]
        elif self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]

        return [permission() for permission in permission_classes]
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_admin:
                print('Admin', self.request.user)
                return self.queryset.all()
            else:
                print('Normal User', self.request.user)
                return self.queryset.filter(user__email=self.request.user.get_username())
        else:
            print('Anonymous User')
            return self.queryset.none()
