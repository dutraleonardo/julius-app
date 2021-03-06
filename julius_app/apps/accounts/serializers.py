from allauth.account.adapter import get_adapter
from allauth.account.utils import setup_user_email
from dj_rest_auth.models import TokenModel
from dj_rest_auth.serializers import TokenSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers

from .models import User, Product, Card, Campaign, Transaction


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = User
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'product_name', 'description', 'user')


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = ('id', 'points', 'user')


class CustomTokenSerializer(TokenSerializer):
    """
    Serializer for Token model.
    """
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = TokenModel
        fields = ('key', 'user')


class CampaignSerializer(serializers.ModelSerializer):
    # product = ProductSerializer(read_only=True)

    class Meta:
        model = Campaign
        fields = ('id', 'campaign_name', 'description', 'points_qty',
                  'product', 'user')

    def to_representation(self, instance):
        """
        This method takes the target of the field as the value argument,
        and should return the representation that should be used
        to serialize the target
        """
        return {
            'id': instance.id,
            'campaign_name': instance.campaign_name,
            'description': instance.description,
            'points_qty': instance.points_qty,
            'product': {
                'id': instance.product.id,
                'product_name': instance.product.product_name,
                'description': instance.product.description
            },
            'user': instance.user.id
        }


class TransactionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Transaction
        fields = ('id', 'value', 'transaction_type', 'user',
                  'card', 'campaign')

    def to_representation(self, instance):
        """
        This method takes the target of the field as the value argument,
        and should return the representation that should be used
        to serialize the target
        """
        return {
            'id': instance.id,
            'transaction_type': instance.transaction_type,
            'value': instance.value,
            'card': {
                'id': instance.card.id,
                'points': instance.card.points,
            },
            'campaign': {
                'id': instance.campaign.id,
                'campaign_name': instance.campaign.campaign_name,
                'description': instance.campaign.description,
                'points_qty': instance.campaign.points_qty,
            },
            'user': instance.user.id
        }


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    account_type = serializers.CharField(write_only=True, required=False)

    def get_cleaned_data(self):
        return {
            'username': self.validated_data.get('username', ''),
            'password1': self.validated_data.get('password1', ''),
            'first_name': self.validated_data.get('first_name', ''),
            'last_name': self.validated_data.get('last_name', ''),
            'account_type': self.validated_data.get('account_type', ''),
            'phone_number': self.validated_data.get('phone_number', ''),
            'cpf_or_cnpj': self.validated_data.get('cpf_or_cnpj', ''),
            'email': self.validated_data.get('email', '')
        }

    def save(self, request):
        if request.data['account_type'] == User.COMPANY:
            request.data['account_type'] = User.COMPANY
        else:
            request.data['account_type'] = User.PERSON
        adapter = get_adapter()
        user = adapter.new_user(request)
        if request.data['account_type'] == User.COMPANY:
            user.account_type = User.COMPANY
        else:
            user.account_type = User.PERSON
        user.cpf_or_cnpj = request.data['cpf_or_cnpj']
        user.phone_number = request.data['phone_number']
        self.cleaned_data = self.get_cleaned_data()
        adapter.save_user(request, user, self)
        self.custom_signup(request, user)
        setup_user_email(request, user, [])
        return user
