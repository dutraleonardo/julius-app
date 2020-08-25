from rest_framework import viewsets, permissions

from .models import User, Product, Card, Campaign, Transaction
from rest_framework import status
from rest_framework.decorators import action
from django.db import transaction, IntegrityError
from rest_framework.response import Response
from .serializers import (UserSerializer, ProductSerializer, CardSerializer,
                          CampaignSerializer, TransactionSerializer
                          )


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CardViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD cards by person users.
    """
    queryset = Card.objects.all().order_by('id')
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if self.request.user.account_type != User.PERSON:
            return Response("You're not a company", status=status.HTTP_400_BAD_REQUEST)
        else:
            user = self.request.user.id
            request.data['user'] = user
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD products by company users.
    """
    queryset = Product.objects.all().order_by('id')
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if self.request.user.account_type != User.COMPANY:
            return Response("You're not a company", status=status.HTTP_400_BAD_REQUEST)
        else:
            user = self.request.user.id
            request.data['user'] = user
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class CampaignViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows CRUD campaign by company users.
    """
    queryset = Campaign.objects.all().order_by('id')
    serializer_class = CampaignSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        if self.request.user.account_type != User.COMPANY:
            return Response("You're not a company", status=status.HTTP_400_BAD_REQUEST)
        else:
            try:
                Product.objects.get(id=self.request.data['product'])
            except Exception:
                return Response("This product doesn't exist!", status=status.HTTP_400_BAD_REQUEST)
            user = self.request.user.id
            request.data['user'] = user
            serializer = self.serializer_class(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows process transation
    """
    queryset = Transaction.objects.all().order_by('id')
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @classmethod
    def process_transaction(cls, card_id, amount):
        with transaction.atomic():
            card = (
                Card.objects
                .select_for_update()
                .get(id=card_id)
            )
            card.points += amount
            card.save()
        return card

    @action(detail=True, methods=['post'])
    def create(self, request, *args, **kwargs):

        # query card and campaign
        try:
            card = Card.objects.get(user_id=request.user.id)
            campaign = Campaign.objects.get(id=request.data['campaign'])
        except Exception as error:
            return Response(error.args[0], status=status.HTTP_400_BAD_REQUEST)

        # check transaction type and create amount to transaction
        if request.data['transaction_type'] == Transaction.REMOVE:
            amount = campaign.points_qty * -1
        elif request.data['transaction_type'] == Transaction.ADD:
            amount = campaign.points_qty
        else:
            return Response("Invalid transaction type", status=status.HTTP_400_BAD_REQUEST)

        request.data['value'] = amount
        request.data['user'] = self.request.user.id
        request.data['card'] = card.id
        try:
            self.process_transaction(card.id, amount)
        except IntegrityError:
            return Response("Transaction refused: you don't have enought points for this transaction",
                            status=status.HTTP_400_BAD_REQUEST)
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
