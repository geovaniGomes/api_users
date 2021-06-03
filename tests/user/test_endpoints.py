from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
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
        self.assertEqual(response.json()['first_name'], self.users[0].first_name)
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

    def test_create_with_groups_and_permissions(self):
        group_create = self.client.post('/groups/',
                                        data={
                                            "name": "grupo one"
                                        })

        permission_create = self.client.post('/permissions/',
            data={
                "name": "create user",
                "code_name": "USER::CREATE"
        })

        response = self.client.post(self.url,
            {
             'username': "leticia@gmail.com",
             'first_name': "leticia",
             'last_name': "almeida",
             'email': "leticia@gmail.com",
             'is_staff': False,
             'password': "52002600NN",
             'permissions': [permission_create.json()],
             'groups': [group_create.json()]
            }, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
