from rest_framework import serializers
from django.contrib.auth import  get_user_model

from rest_framework.authtoken.models import Token

User = get_user_model()


class UserLoginSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'username',
            'email',
            'bio',
            'gender',
            'token',
        ]

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'image',
            'username',
            'email',
            'bio',
            'gender'
        ]