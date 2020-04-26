# # # 
# Taken from Francois's code in apf
# TODO ask and acknowledge if needed
# 

import os
import pytz
from datetime import datetime
from django.conf import settings
from django.test import TestCase
from django_webtest import WebTest
from django.contrib.auth.models import User

utc = pytz.utc

def get_1_january_2014():
    return datetime(year=2014, day=1, month=1, hour=12, minute=10, second=0, tzinfo=utc)


def get_1_march_2014():
    return datetime(year=2014, day=1, month=3, hour=12, minute=10, second=0, tzinfo=utc)


class SimpleTest(TestCase):
    """
    Based on django TestCase
    adapted for unit tests and functional tests not involving forms / users logged-in etc.
    """

    # no fixtures - use factory_boy instead
    # fixtures = []

    def assert_page_loading(self, path, status_code=200, method="GET", data=None):
        if method == "OPTIONS":
            response = self.client.options(path=path)

        if method == "GET":
            response = self.client.get(path=path)

        if method == "PUT":
            response = self.client.put(path=path, data=data)

        self.assertEqual(response.status_code, status_code)
        return response

    def _streaming_response_to_string(self, response):
        result = ""
        content = response.streaming_content
        for c in content:
            result += c

        return result


class RegularTest(WebTest):
    """
    Based on WebTest
    for all other tests
    """

    # no fixtures - use factory_boy instead

    def assert_page_loading(self, path, status_code=200, user=None, server_name="mydomain.com", extra_environ=None):
        return self.app.get(url=path, status=status_code, user=user,
                            headers={'SERVER_NAME': server_name, 'HOST': server_name}, extra_environ=extra_environ)

    def assert_page_post(self, path, status_code=200, user=None, server_name="mydomain.com", params='', extra_environ=None):
        return self.app.post(url=path, status=status_code, user=user,
                            headers={'SERVER_NAME': server_name, 'HOST': server_name},
                            params=params)

    def assert_page_redirecting_to(self, path, redirect_to, user=None, status_code=302, follow_redirection=False, extra_environ=None):
        """
        Check that the page is loading with the correct redirection status code and Location parameter
        return that response (after following the redirection if required)
        """
        response = self.assert_page_loading(user=user, path=path, status_code=status_code, extra_environ=extra_environ)
        actual_redirection = response['Location']

        if not redirect_to in actual_redirection:
            raise self.failureException(
                "Redirection must contain: %s . Actual redirection: %s" % (redirect_to, actual_redirection))

        if follow_redirection:
            return response.follow()
        else:
            return response

    def assert_exception_message(self, raise_context, message):
        exception = raise_context.exception

        self.assertIn(member=message, container=str(exception))

    def get_testing_image(self):
        image_name = '_test-image.jpg'
        image_file_name = 'test.jpg'

        return (
            image_name,
            file(os.path.join(settings.TEST_FILES_PATH, "images", image_file_name)).read()
        )

    def get_testing_bmp(self):
        image_name = '_test-image.bmp'
        image_file_name = 'test.bmp'

        return (
            image_name,
            file(os.path.join(settings.TEST_FILES_PATH, "images", image_file_name)).read()
        )
