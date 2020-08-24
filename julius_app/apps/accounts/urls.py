from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter
from dj_rest_auth.registration import urls
from .views import UserViewSet, ProductViewSet, CardViewSet

BASE_URL = 'juliusapp'

router = SimpleRouter()

router.register('users', UserViewSet, 'user')

product_list = ProductViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
product_detail = ProductViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

card_list = CardViewSet.as_view({
    'post': 'create'
})
card_detail = CardViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

urlpatterns = [
    path('', include(router.urls)),
    path(f'{BASE_URL}/', include('dj_rest_auth.urls')),
    path(f'{BASE_URL}/registration/', include('dj_rest_auth.registration.urls')),
    path(f'{BASE_URL}/password/reset/', views.PasswordResetView.as_view(), name='password_reset'),
    path(f'{BASE_URL}/password/reset/done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path(
        f'{BASE_URL}/reset/<uidb64>/<token>/',
        views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    path(f'{BASE_URL}/user/product/', product_list, name='product_list'),
    path(f'{BASE_URL}/user/product/<int:pk>/', product_detail, name='product_detail'),
    path(f'{BASE_URL}/user/card/', card_list, name='card_list'),
    path(f'{BASE_URL}/user/card/<int:pk>/', card_detail, name='card_detail'),
    path(f'{BASE_URL}/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
