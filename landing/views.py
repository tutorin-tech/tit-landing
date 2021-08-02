"""A module that contains the class-based views related to the landing application. """

from django.urls import reverse
from django.views.generic import RedirectView, TemplateView

from .api_client import request_courses
from .exceptions import CoursesRequestFailed


class MainPage(TemplateView):
    """The main page view. """

    template_name = 'pages/main.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            context['courses'] = request_courses()
        except CoursesRequestFailed:
            context['courses'] = None

        return context


class PrivacyPolicy(TemplateView):
    """The privacy-policy page view. """

    template_name = 'pages/privacy-policy.html'


class SignOut(RedirectView):
    """Class-based view implementing signing out of an account. """

    def dispatch(self, request, *args, **kwargs):
        try:
            self.url = request.POST['next']
        except KeyError:
            self.url = reverse('main-page')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        response.delete_cookie('accessToken')
        response.delete_cookie('refreshToken')

        return response


class TermsOfUse(TemplateView):
    """The terms-of-use page view. """

    template_name = 'pages/terms-of-use.html'
