"""The URL configuration for the landing application. """

from django.urls import re_path

from .views import MainPage

urlpatterns = [
    re_path(r'^$', MainPage.as_view(), name='main-page'),
]
