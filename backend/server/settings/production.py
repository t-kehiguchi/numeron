from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '-()$c@ul2jxaob3=354(dc8ypmc=_c^hfr!5!v_ab11m_^#mik'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'heroku_4d412989052757a',
        'USER': 'bc391bee64ee4a',
        'PASSWORD': 'cc59f15a',
        'HOST': 'us-cdbr-east-06.cleardb.net',
        'PORT': '3306',
    }
}
