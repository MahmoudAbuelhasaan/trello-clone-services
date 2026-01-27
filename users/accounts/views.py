from .models import User, UserProfile
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRigisterSerializer,UserSerializer
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .tasks import send_welcome_email


class UserRegisterationView(APIView):
    """API view for user registration."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRigisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Trigger the welcome email task
            send_welcome_email.delay({'id': user.id, 'email': user.email})
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "User registered successfully.",
                'user': UserSerializer(user).data,
                "token": {
                "refresh": str(refresh), 
                "access": str(refresh.access_token)
                }
            }, status=status.HTTP_201_CREATED)
         
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    