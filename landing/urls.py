"""The URL configuration for the landing application. """

from django.urls import re_path

from .views import MainPage, PrivacyPolicy, SignOut, TermsOfUse

urlpatterns = [
    re_path(r'^$', MainPage.as_view(), name='main-page'),
    re_path(r'^privacy-policy/?$', PrivacyPolicy.as_view(), name='privacy-policy'),
    re_path(r'^sign-out/?$', SignOut.as_view(), name='sign-out'),
    re_path(r'^terms-of-use/?$', TermsOfUse.as_view(), name='terms-of-use'),
]
