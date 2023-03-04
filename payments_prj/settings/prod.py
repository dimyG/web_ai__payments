from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend'
