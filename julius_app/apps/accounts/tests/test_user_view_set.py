import pytest
from rest_framework.reverse import reverse
from rest_framework.test import force_authenticate

from ..views import UserViewSet


@pytest.fixture
def create_user_view():
    def make_view(actions):
        return UserViewSet.as_view(actions)

    return make_view


@pytest.mark.django_db
def test_list_users(create_user, create_user_view, factory):
    user = create_user()
    url = reverse('user-list')
    request = factory.get(url)
    force_authenticate(request, user=user)
    view = create_user_view({'get': 'list'})
    response = view(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_create_users(create_user, create_user_view, factory):
    user = create_user()
    url = reverse('user-list')
    request = factory.post(url, {'email': 'email@example.com', 'first_name': 'John', 'password': 'password'})
    force_authenticate(request, user=user)
    view = create_user_view({'post': 'create'})
    response = view(request)
    assert response.status_code == 201


@pytest.mark.django_db
def test_update_users(create_user, create_user_view, factory):
    user = create_user()
    url = reverse('user-detail', kwargs={'pk': user.pk})
    request = factory.put(url, {'first_name': 'Paul'})
    force_authenticate(request, user=user)
    view = create_user_view({'put': 'update'})
    response = view(request, pk=user.pk)
    assert response.status_code == 200
    assert response.data['first_name'] == 'Paul'


@pytest.mark.django_db
def test_retrieve_users(create_user, create_user_view, factory):
    user = create_user()
    url = reverse('user-detail', kwargs={'pk': user.pk})
    request = factory.get(url)
    force_authenticate(request, user=user)
    view = create_user_view({'get': 'retrieve'})
    response = view(request, pk=user.pk)
    assert response.status_code == 200


@pytest.mark.django_db
def test_delete_users(create_user, create_user_view, factory):
    user = create_user()
    url = reverse('user-detail', kwargs={'pk': user.pk})
    request = factory.delete(url)
    force_authenticate(request, user=user)
    view = create_user_view({'delete': 'destroy'})
    response = view(request, pk=user.pk)
    assert response.status_code == 204
