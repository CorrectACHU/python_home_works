from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, help_text="пароль", label="Password", write_only=True,
    )

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
