from django.contrib.auth import login
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, UserProfile
from .serializers import UserRigisterSerializer, UserSerializer, loginSerializer
from .tasks import send_welcome_email


class UserRegisterationView(APIView):
    """API view for user registration."""

    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Email address",
            ),
            openapi.Parameter(
                "username",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Username",
            ),
            openapi.Parameter(
                "first_name",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="First name",
            ),
            openapi.Parameter(
                "last_name",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=False,
                description="Last name",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Password (min 8 characters)",
            ),
            openapi.Parameter(
                "password_confirm",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Confirm password",
            ),
        ],
        consumes=["multipart/form-data", "application/x-www-form-urlencoded"],
    )
    def post(self, request):
        serializer = UserRigisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Trigger the welcome email task
            send_welcome_email.delay({"id": user.id, "email": user.email})
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User registered successfully.",
                    "user": UserSerializer(user).data,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """API view for user login."""
    serializers_class = loginSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [FormParser, JSONParser]

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                "email",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Email address",
            ),
            openapi.Parameter(
                "password",
                openapi.IN_FORM,
                type=openapi.TYPE_STRING,
                required=True,
                description="Password",
            ),
        ],
        consumes=["application/x-www-form-urlencoded"],
    )
    def post(self, request):
        serializer = loginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data.get("user")
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "message": "User login successfully.",
                    "user": UserSerializer(user).data,
                    "token": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
