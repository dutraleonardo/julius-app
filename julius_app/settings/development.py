from .base import *  # noqa

CORS_ORIGIN_ALLOW_ALL = True

# See https://docs.djangoproject.com/en/2.2/topics/cache/#dummy-caching-for-development
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache"
    }
}

# See https://docs.djangoproject.com/en/2.2/topics/email/#console-backend
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


INSTALLED_APPS.insert(0, 'whitenoise.runserver_nostatic')
