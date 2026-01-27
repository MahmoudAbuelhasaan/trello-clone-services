from django.urls import path
from .views import UserRegisterationView
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns = [
    path('register/', UserRegisterationView.as_view(), name='user_register'),

]
