from rest_framework import viewsets, permissions

from .models import User, Product, Card
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, ProductSerializer, CardSerializer


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
