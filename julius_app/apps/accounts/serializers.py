from dj_rest_auth.models import TokenModel
from dj_rest_auth.serializers import TokenSerializer
from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'


class CustomTokenSerializer(TokenSerializer):
    """
    Serializer for Token model.
    """
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')
