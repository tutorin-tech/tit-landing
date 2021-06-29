"""A module that contains the class-based views related to the landing application. """

from django.views.generic import TemplateView

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
