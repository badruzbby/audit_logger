from django.shortcuts import render
from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.utils import timezone
from datetime import timedelta
import uuid
import hashlib

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    LoginSerializer,
    UserAPIKeySerializer
)
from .models import UserAPIKey

# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'user': UserSerializer(user).data
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAPIKeyViewSet(viewsets.ModelViewSet):
    serializer_class = UserAPIKeySerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return UserAPIKey.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        # Generate a new API key
        key = uuid.uuid4().hex + uuid.uuid4().hex
        hashed_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
        
        # Default expiry of 1 year if not specified
        expires = None
        if 'expires_in_days' in self.request.data:
            try:
                days = int(self.request.data['expires_in_days'])
                expires = timezone.now() + timedelta(days=days)
            except ValueError:
                pass
        
        instance = serializer.save(
            user=self.request.user,
            key=hashed_key,
            expires=expires,
            is_active=True
        )
        
        # Return the unhashed key only once
        self.unhasked_key = key
    
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        response.data['key'] = self.unhasked_key
        return response
