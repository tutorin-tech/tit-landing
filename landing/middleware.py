# Copyright 2021 Artem Lavruhin. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and

"""Module containing the middlewares for landing application. """

import jwt
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.utils.deprecation import MiddlewareMixin

from .api_client import WhoAmI

REFRESH_TOKEN_SESSION_KEY = '_refresh_token'
USER_SESSION_KEY = '_auth_user'


def token_has_expired(encoded_token):
    """Checks if a TIT API token (either access or refresh) has expired. """

    try:
        jwt.decode(encoded_token, settings.SECRET_KEY, settings.JWT_ALGORITHM)
        return False
    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidSignatureError, ):
        return True


def get_user(request):
    """Returns either TITUser (from session or TIT API) or AnonymousUser. """

    refresh_token = request.COOKIES.get(settings.REFRESH_TOKEN_COOKIE_KEY)
    session_refresh_token = request.session.get(REFRESH_TOKEN_SESSION_KEY)

    if refresh_token == session_refresh_token and not token_has_expired(refresh_token):
        user_dict = request.session[USER_SESSION_KEY]
    else:
        user_dict = WhoAmI(request)
        if user_dict:
            request.session[USER_SESSION_KEY] = user_dict
            request.session[REFRESH_TOKEN_SESSION_KEY] = refresh_token

    if user_dict:
        return TITUser(user_dict)

    return AnonymousUser()


class TITUser:
    """Class representing an authenticated user. """

    def __init__(self, user):
        self.__dict__.update(user)

    @property
    def is_anonymous(self):
        """Checks if the user is anonymous. """

        return False

    @property
    def is_authenticated(self):
        """Checks if the user is authenticated. """

        return True

    def __str__(self):
        return 'TITUser'


class UserAuthenticationMiddleware(MiddlewareMixin):
    """Overrides the Django AuthenticationMiddleware built-in middleware. """

    def process_request(self, request):  # pylint: disable=no-self-use
        """Processes the request. """

        assert hasattr(request, 'session'), (
            "Authentication middleware requires session middleware to be installed."
        )

        request.user = get_user(request)
