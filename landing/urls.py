"""The URL configuration for the landing application. """

from django.urls import re_path

from .views import MainPage, SignOut

urlpatterns = [
    re_path(r'^$', MainPage.as_view(), name='main-page'),
    re_path(r'^sign-out/?$', SignOut.as_view(), name='sign-out'),
]
