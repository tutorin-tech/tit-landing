"""Module indented to extend and override settings.py via the environment variables. """

import os

from conf.settings import *  # pylint: disable=unused-wildcard-import,wildcard-import

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '127.0.0.1').split(',')

DEBUG = os.getenv('DEBUG', '').lower() == 'true'

SECRET_KEY = os.environ['SECRET_KEY']

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL', 'http://localhost:8004/')

TIT_API_HOST = os.environ.get('TIT_API_HOST', 'http://127.0.0.1:8003')
