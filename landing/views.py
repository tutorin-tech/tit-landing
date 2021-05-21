"""A module that contains the class-based views related to the landing application. """

from django.views.generic import TemplateView


class MainPage(TemplateView):
    """The main page view. """

    template_name = 'pages/main.html'
