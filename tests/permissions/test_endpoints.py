from rest_framework import status
from rest_framework.test import APITestCase

from .factories import PermissionFactory
from permissions.models import CustomPermission

class TestPermissionEndpoints(APITestCase):
    def test_list_empty(self):
        data = []
        url = '/permissions/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)