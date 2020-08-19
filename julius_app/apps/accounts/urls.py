from django.contrib.auth import views
from django.urls import path, include
from rest_framework.routers import SimpleRouter

from .views import UserViewSet

BASE_URL = 'dj-rest-auth'

router = SimpleRouter()

router.register('users', UserViewSet, 'user')

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
    path(f'{BASE_URL}/reset/done/', views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
