from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# todo: remove cors headers wehn you set up a custom domain name for the API Gateway
INSTALLED_APPS.insert(0, 'corsheaders')
MIDDLEWARE.insert(0, 'corsheaders.middleware.CorsMiddleware')  # not ASGI compatible

CORS_ALLOW_ALL_ORIGINS = True

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
