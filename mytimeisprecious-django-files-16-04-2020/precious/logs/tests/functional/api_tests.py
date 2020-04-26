from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class APIHourTests(APITestCase):
    def test_create_hour(self):
        """
        Ensure we can create a new hour object.
        """
        url = reverse('hour-detailed')
        data = {'hour_text': 'Testing api'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
