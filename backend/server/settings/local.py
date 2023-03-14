from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-6^2i72t#788b9=pe19b5o+99ntm+$vz0fq&881&n1n9v%^b=o3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'numeron',
        'USER': 't-kehiguchi',
        'PASSWORD': 't0tp50gx',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
