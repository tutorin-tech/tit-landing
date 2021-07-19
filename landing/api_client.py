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

from urllib.error import HTTPError
from urllib.parse import urljoin

import requests
from django.conf import settings
from requests.exceptions import ConnectionError

from .exceptions import CoursesRequestFailed

SUCCEEDED_STATUS = 200
UNAUTHORIZED_STATUS = 401


def request_courses():
    """Requests a courses list using the TiT API. """

    url = urljoin(settings.TIT_API_HOST, f'/api/course/')

    try:
        response = requests.get(url)
        response.raise_for_status()
    except (ConnectionError, ConnectionRefusedError, HTTPError, ) as exc:
        raise CoursesRequestFailed from exc

    return response.json()


def get_authorization_header(request):
    """Returns the dict with Authorization header for using in a request to TIT API. """

    try:
        access_token = request.COOKIES['accessToken']
        return {'Authorization': f'Bearer {access_token}'}
    except KeyError:
        """Access token doesn't exist in cookies. """

    return None


def refresh_access_token_deco(func):
    """Decorator for re-request with a refreshing access token.
    * Calls the api function, which makes a request to TIT API.
    * Refreshes the access token if first request to TIT API returns 401 status code.
    * Calls the api function with refreshing access token.
    """

    def wrapper(request, *args, **kwargs):
        result = None

        try:
            result = func(request, *args, **kwargs)
        except requests.HTTPError as exc:
            if exc.response.status_code == UNAUTHORIZED_STATUS:
                refresh_result = refresh_access_token(request)

                if refresh_result:
                    try:
                        result = func(request, *args, **kwargs)
                    except requests.HTTPError:
                        """Retry request failed. """

        return result

    return wrapper


def refresh_access_token(request):
    """Updates `accessToken` in request cookies (not in browser cookies) using `refreshToken`. """

    try:
        refresh_token = request.COOKIES['refreshToken']
        url = urljoin(settings.TIT_API_HOST, '/api/auth/token/refresh/')

        response = requests.post(url, {'refresh': refresh_token})

        result = response.json()
        request.COOKIES['accessToken'] = result['access']

        return True
    except (KeyError, requests.HTTPError, ):
        """Refresh token doesn't exist in cookies or response from TIT API
        returned error status code.
        """

    return False


@refresh_access_token_deco
def WhoAmI(request):
    """Makes a request to the TIT API `whoami` endpoint for getting the current user. """

    headers = get_authorization_header(request)
    url = urljoin(settings.TIT_API_HOST, '/api/auth/whoami/')

    try:
        response = requests.get(url, headers=headers)
    except requests.ConnectionError:
        return None

    response.raise_for_status()  # Raised for _refresh_access_token_deco

    if response.status_code == SUCCEEDED_STATUS:
        return response.json()

    return None
