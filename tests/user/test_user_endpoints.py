from rest_framework import status
from rest_framework.test import APITestCase
from .factories import UserFactory, SuperUserFactory

from users.models import User


class TestUserEndpoint(APITestCase):
    def test_list_empty(self):
        """
        Ensure we can create a new account object.
        """
        data = []
        url = '/users/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_create_empty(self):
        url = '/users/'
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create(self):
        url = '/users/'
        factory_data = UserFactory
        response = self.client.post(
            url, {'username': factory_data.username}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], factory_data.username)
        self.assertEqual(response.json()['is_staff'], factory_data.is_staff)

    def test_create_superuser(self):
        url = '/users/'
        factory_data = SuperUserFactory

        response = self.client.post(
            url,
            {'username': factory_data.username,
             'is_staff': factory_data.is_staff
             }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], factory_data.username)
        self.assertEqual(response.json()['is_staff'], factory_data.is_staff)

    def test_create_username_duplicate(self):
        url = '/users/'
        factory_data = UserFactory
        self.client.post(
            url, {'username': factory_data.username}
        )
        response = self.client.post(
            url, {'username': factory_data.username}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_email_duplicate(self):
        url = '/users/'
        factory_data = UserFactory
        self.client.post(
            url, {'username': factory_data.username,
                  'email': factory_data.email}
        )
        response = self.client.post(
            url, {'username': factory_data.username,
                  'email': factory_data.email}
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_permission_empty(self):
        url = "/users/"
        factory_data = UserFactory

        self.client.post(
            url, {'username': factory_data.username,
                  'email': factory_data.email
                  })
        user = User.objects.all()[0]
        url_update = f"{url}{user.id}/"

        response = self.client.put(
            url_update,
            {'username': factory_data.username,
             'email': factory_data.email,
             'first_name': factory_data.first_name
             }
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_username_empty(self):
        url = "/users/"
        factory_data = UserFactory

        self.client.post(
            url, {'username': factory_data.username,
                  'email': factory_data.email
                  })
        user = User.objects.all()[0]
        url_update = f"{url}{user.id}/"

        response = self.client.put(
            url_update,
            {
             'email': factory_data.email,
             'first_name': factory_data.first_name
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLogin(APITestCase):


    def test_login(self):
        url_auth = '/token/'
        url = '/users/'
        factory_data = UserFactory
        self.client.post(
            url, {'username': factory_data.username,
                  'password': '520002600nn'}
        )

        response = self.client.post(
            url_auth,
            {
                'username': factory_data.username,
                'password': '520002600nn'
            })
        self.assertEqual(response.status_code, status.HTTP_200_OK)


