import re

from .base import *  # noqa

CSRF_COOKIE_SECURE = True

SESSION_COOKIE_SECURE = True

# In your .env file add your administrators as in the example:
# ADMINS="'(\"Your Name\", \"email@example.com\")','(\"Your Name\", \"email@example.com\")'"
# https://docs.djangoproject.com/en/2.2/ref/settings/#admins
ADMINS = config('ADMINS', cast=lambda admins: [eval(admin) for admin in Csv()(admins)])

MANAGERS = ADMINS

IGNORABLE_404_URLS = [
    re.compile(r'^/apple-touch-icon.*\.png$'),
    re.compile(r'^/favicon.ico$'),
    re.compile(r'^/robots.txt$'),
    re.compile(r'^/phpmyadmin/'),
    re.compile(r'\.(cgi|php|pl)$'),
]

EMAIL_HOST = config('EMAIL_HOST', default='localhost')
EMAIL_PORT = config('EMAIL_PORT', default=25, cast=int)
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=False, cast=bool)

CORS_ORIGIN_WHITELIST = config('CORS_ORIGIN_WHITELIST', cast=Csv())
