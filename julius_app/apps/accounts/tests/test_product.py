from django.urls import reverse
from rest_framework import status
from rest_framework.test import force_authenticate, APIRequestFactory, APITestCase

from ..views import ProductViewSet
from julius_app.apps.accounts.models import User, Product


class ProductModelViewSet(APITestCase):
    def setUp(self):
        self.john = User.objects.create(
            first_name='John',
            last_name='Doe',
            email='johndoe@juliusapp.com',
            cpf_or_cnpj='34648828020',
            phone_number='8599993456',
            account_type=User.PERSON
        )
        self.charles_darwin = User.objects.create(
            first_name='Charles Darwin',
            last_name=' Co.',
            email='contato@charlesdarwin.com',
            cpf_or_cnpj='11055022000175',
            phone_number='85999830666',
            account_type=User.COMPANY
        )
        self.data = {
            'product_nam': 'On the Origin of Species by Means of Natural Selection',
            'description': 'Amazing book'
        }
        self.factory = APIRequestFactory()

    def test_create_product_with_person(self):
        url = reverse('user-list')
        self.data['user'] = self.john.id
        request = self.factory.post(url, self.data, format='json')
        view = ProductViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.john)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_product_with_company(self):
        url = reverse('user-list')
        self.data['user'] = self.charles_darwin.id
        request = self.factory.post(url, self.data, format='json')
        view = ProductViewSet.as_view({'post': 'create'})
        force_authenticate(request, self.charles_darwin)
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
