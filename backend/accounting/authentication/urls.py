from django.contrib import admin
from django.urls import path
from .views import LogoutView, RegistrationAPIView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationAPIView.as_view(), name='register'),
]
