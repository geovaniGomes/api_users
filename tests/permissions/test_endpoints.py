from rest_framework import status
from rest_framework.test import APITestCase
from .factories import PermissionFactory
from core.models import Permission

'''
class TestPermissionEndpoints(APITestCase):
    url = '/permissions/'

    def test_list_empty(self):
        data = []

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def create(self):
        factory_data = PermissionFactory
        response = self.client.post(
            self.url,
            {
                "name": factory_data.name,
                "code_name": factory_data.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def create_code_name_empty(self):
        factory_data = PermissionFactory
        response = self.client.post(
            self.url,
            {
                "name": factory_data.name
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_name_empty(self):
        factory_data = PermissionFactory
        response = self.client.post(
            self.url,
            {
                "code_name": factory_data.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def create_duplicated(self):
        factory_data = PermissionFactory
        self.client.post(
            self.url,
            {
                "name": factory_data.name,
                "code_name": factory_data.code_name
            })
        factory_data = PermissionFactory

        response = self.client.post(
            self.url,
            {
                "name": factory_data.name,
                "code_name": factory_data.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def update(self):
        factory_data = PermissionFactory
        response_create = self.client.post(
            self.url,
            {
                "name": factory_data.name,
                "code_name": factory_data.code_name
            })

        response = self.client.put(
            self.url+response_create.json()['id'],
           {
               "name": "Delete user",
               "code_name":"USER::ACTION:DELETE"
           })
        self.assertEqual(response.json()['name'], "Delete user")
        self.assertEqual(response.json()['code_name'], "USER::ACTION:DELETE")

    def delete(self):
        factory_data = PermissionFactory
        response_create = self.client.post(
            self.url,
            {
                "name": factory_data.name,
                "code_name": factory_data.code_name
            })

        response = self.client.delete(self.url+response_create.json()['id'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)

'''