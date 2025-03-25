from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from google.auth.transport import requests
from google.oauth2 import id_token
import os

from backend.models import User  # Ensure this comes after Django imports
from backend.serializers import UserSerializer  # Import after defining models


class SignupView(APIView):
    def post(self, request):
        print("Request Data:", request.data)  # Debugging print

        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')

        if not email or not username or not password:
            return Response({'error': 'Email, username, and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure unique username
        if User.objects.filter(username=username).exists():
            return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

        # Ensure unique email
        if User.objects.filter(email=email).exists():
            return Response({'error': 'Email already registered'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)
        return Response(user.get_tokens(), status=status.HTTP_201_CREATED)

from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login
from backend.models import User  
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from backend.models import User


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            "id": user.id,
            "email": user.email,
            "username": user.username,
        })
    
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    return Response({
        "id": request.user.id,
        "email": request.user.email,
        "username": request.user.username,
    })



class LoginView(APIView):
    def post(self, request):
        email_or_username = request.data.get("email_or_username")
        password = request.data.get("password")

        if not email_or_username or not password:
            return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=email_or_username, password=password)

        if user is not None:
            login(request, user)  # ✅ Log in user (for session-based auth)
            refresh = RefreshToken.for_user(user)

            # ✅ Store tokens in session
            request.session["access_token"] = str(refresh.access_token)
            request.session["refresh_token"] = str(refresh)

            # ✅ Send token response (NO REDIRECT)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username
                }
            }, status=status.HTTP_200_OK)

        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from google.auth.transport import requests
from google.oauth2 import id_token
import os
from .models import User

class GoogleAuthView(APIView):
    def post(self, request):
        token = request.data.get("token")
        if not token:
            return Response({"error": "Token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Verify Google token
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), os.getenv("GOOGLE_CLIENT_ID"))

            email = idinfo["email"]
            username = idinfo.get("name", email.split("@")[0])  # Use name if available, otherwise generate from email

            # Check if user exists, if not, create them
            user, created = User.objects.get_or_create(
                email=email,
                defaults={"username": username, "google_id": idinfo["sub"]}
            )

            return Response(user.get_tokens(), status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"error": "Invalid Google token"}, status=status.HTTP_400_BAD_REQUEST)

