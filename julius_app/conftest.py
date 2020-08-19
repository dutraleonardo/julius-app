import pytest


@pytest.fixture
def factory():
    from rest_framework.test import APIRequestFactory
    return APIRequestFactory()
