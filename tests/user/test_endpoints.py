from rest_framework import status
from rest_framework.test import APITestCase
from .factories import UserFactory, SuperUserFactory, UserSecondaryFactory
from core.models import User


class TestUserEndpoint(APITestCase):
    url = '/users/'
    users = User.objects.all()
    primary_user_factory = UserFactory
    seconder_user_factory = UserSecondaryFactory

    def test_list_empty(self):
        data = []
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, data)

    def test_create_empty(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_valid(self):
        response = self.client.post(
            self.url,
            {'username': self.primary_user_factory.username,
             'first_name': self.primary_user_factory.first_name,
             'last_name': self.primary_user_factory.last_name,
             'email': self.primary_user_factory.email,
             'is_staff': self.primary_user_factory.is_staff,
             'password': self.primary_user_factory.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], self.primary_user_factory.username)
        self.assertEqual(response.json()['is_staff'], self.primary_user_factory.is_staff)
        return response

    def test_create_superuser(self):

        response = self.client.post(
            self.url,
            {'username': self.primary_user_factory.username,
             'first_name': self.primary_user_factory.first_name,
             'last_name': self.primary_user_factory.last_name,
             'email': self.primary_user_factory.email,
             'is_staff': self.primary_user_factory.is_staff,
             'password': self.primary_user_factory.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], self.primary_user_factory.username)
        self.assertEqual(response.json()['is_staff'], self.primary_user_factory.is_staff)

    def test_create_username_duplicate(self):
        response_create = self.test_create_valid()

        response = self.client.post(
            self.url,
            {'username': response_create.json()['username'],
             'first_name': self.primary_user_factory.first_name,
             'last_name': self.primary_user_factory.last_name,
             'email': self.seconder_user_factory.email,
             'is_staff': self.primary_user_factory.is_staff,
             'password': self.primary_user_factory.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_email_duplicate(self):
        response_create = self.test_create_valid()

        response = self.client.post(
            self.url,
            {'username': self.seconder_user_factory.username,
             'first_name': self.primary_user_factory.first_name,
             'first_name': self.primary_user_factory.last_name,
             'email': response_create.json()['email'],
             'is_staff': self.primary_user_factory.is_staff,
             'password': self.primary_user_factory.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_valid(self):
        create_response = self.test_create_valid()
        url_update = f"{self.url}{create_response.json()['id']}/"
        data = self.client.get(url_update)

        response = self.client.put(
            url_update,
            {'username': data.json()['username'],
             'first_name': self.seconder_user_factory.first_name,
             'last_name': self.seconder_user_factory.last_name,
             'email': data.json()['email'],
             'is_staff': data.json()['is_staff']
             }
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], self.users[0].fris_name)
        self.assertEqual(response.json()['last_name'], self.users[0].last_name)

    def test_update_username_empty(self):

        create_response = self.test_create_valid()

        url_update = f"{self.url}{create_response.json()['id']}/"
        data = self.client.get(url_update)
        response = self.client.put(
            url_update,
            {
                'first_name': data.json()['first_name'],
                'last_name': data.json()['last_name'],
                'email': data.json()['email'],
                'is_staff': data.json()['is_staff']
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

"""
class UserLogin(APITestCase):

    def test_login(self):
        url_auth = '/token/'
        url = '/users/'
        factory_data = SuperUserFactory
        data_1 = self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        self.assertEqual(data_1.status_code, status.HTTP_201_CREATED)
        from rest_framework_simplejwt.tokens import RefreshToken
        user = User.objects.all()[0]
        refresh = RefreshToken.for_user(user)
        response = self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        token = response.data['token']
        data = self.client.get(url)
        print(data)
"""