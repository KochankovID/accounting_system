from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer


class RegistrationSerializer(ModelSerializer):
    """ Сериализация регистрации пользователя и создания нового. """
    email = serializers.EmailField(
        required=True,
    )

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True,
    )

    class Meta:
        model = User
        fields = ['email', 'username', 'password']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)