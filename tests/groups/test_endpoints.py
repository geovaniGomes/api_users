from rest_framework import status
from rest_framework.test import APITestCase
from .factories import GroupFactory
from core.models import Group


class TestGroupEndpoints(APITestCase):
    url = "/groups/"
    first_group = GroupFactory
    second_group = GroupFactory
    group = Group.objects.all()

    def test_list_empty(self):
        data = []
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), data)

    def test_create_empty(self):
        response = self.client.post(self.url, data={"name": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid(self):
        response = self.client.post(self.url,
                                    data={
                                        "name": self.first_group.name
                                    })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['name'], self.group[0].name)
        return response

    def test_list_populated(self):
        self.test_create_valid()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert len(response.json()) > 0

    def test_update_invalid(self):
        response_create = self.test_create_valid()
        response = self.client.put(f"{self.url+response_create.json()['id']}/",
                                   data={
                                       "id": response_create.json()['id'],
                                       "name": ""
                                   })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid(self):
        response_create = self.test_create_valid()
        response = self.client.put(f"{self.url+response_create.json()['id']}/",
                                   data={
                                       "id": response_create.json()['id'],
                                       "name": self.second_group.name
                                   })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['name'], self.group[0].name)

    def test_inactivate(self):
        response_create = self.test_create_valid()
        response = self.client.delete(f"{self.url+response_create.json()['id']}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
