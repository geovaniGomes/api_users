from rest_framework import status
from rest_framework.test import APITestCase
from .factories import PermissionFactory, PermissionWithGroup
from tests.groups.test_endpoints import TestGroupEndpoints
from core.models import Permission, Group


class TestPermissionEndpoints(APITestCase):
    url = '/permissions/'
    permissions = Permission.objects.all()
    permission_factory = PermissionFactory
    second_permission_factory = PermissionFactory
    permission_group_factory = PermissionWithGroup
    groups = Group.objects.all()

    def test_list_empty(self):
        data = []

        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_create_invalid(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid(self):
        response = self.client.post(
            self.url,
            {
                "name": self.permission_factory.name,
                "code_name": self.permission_factory.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['code_name'], self.permissions[0].code_name)
        return response

    def create_code_name_empty(self):
        response = self.client.post(
            self.url,
            {
                "name": self.permission_factory.name
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_name_empty(self):
        response = self.client.post(
            self.url,
            {
                "code_name": self.permission_factory.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_duplicated(self):
        self.test_create_valid()

        response = self.client.post(self.url,
                                    data={
                                        "name": self.permission_factory.name,
                                        "code_name": self.permission_factory.code_name
                                    })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_invalid(self):
        response_create = self.test_create_valid()

        response = self.client.put(
            f"{self.url+response_create.json()['id']}/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_codeName_empty(self):
        response_create = self.test_create_valid()

        response = self.client.put(
            f"{self.url+response_create.json()['id']}/",
            data={
                "name": response_create.json()['name'],
                "code_name": ""
            })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid(self):
        response_create = self.test_create_valid()
        response = self.client.put(
            f"{self.url + response_create.json()['id']}/",
            data={
                "name": self.second_permission_factory.name,
                "code_name": self.second_permission_factory.code_name
            })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.permissions[0].name)
        self.assertEqual(response.json()['code_name'], self.permissions[0].code_name)

    def test_create_with_groups(self):
        create_response = self.client.post("/groups/",
                                           data={"name": "group one"})

        self.assertEqual(create_response.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            self.url,
            data={
                "name": self.permission_group_factory.name,
                "code_name": self.permission_group_factory.code_name,
                "groups": [create_response.json()]
            },
            format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response

    def test_remove_groups(self):

        create_response = self.test_create_with_groups()

        response = self.client.put(
            f"{self.url+ create_response.json()['id']}/",
            data={
                "name": self.permission_group_factory.name,
                "code_name": self.permission_group_factory.code_name
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['groups'], [])

    def test_inactivate(self):
        response_create = self.test_create_valid()
        response = self.client.delete(
            f"{self.url + response_create.json()['id']}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
