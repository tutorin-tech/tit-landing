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


def request_courses():
    """Requests a courses list using the TiT API. """

    url = urljoin(settings.TIT_API_HOST, f'/api/course/')

    try:
        response = requests.get(url)
        response.raise_for_status()
    except (ConnectionError, ConnectionRefusedError, HTTPError, ) as exc:
        raise CoursesRequestFailed from exc

    return response.json()
