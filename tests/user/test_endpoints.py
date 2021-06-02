from rest_framework import status
from rest_framework.test import APITestCase
from .factories import UserFactory, SuperUserFactory
from core.models import User

'''
class TestUserEndpoint(APITestCase):
    def test_list_empty(self):
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
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name':factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
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
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json()['username'], factory_data.username)
        self.assertEqual(response.json()['is_staff'], factory_data.is_staff)

    def test_create_username_duplicate(self):
        url = '/users/'
        factory_data = UserFactory(email='usuario@gmail.com')
        self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        response = self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': "carlosmelo@gmail.ccom",
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_email_duplicate(self):
        url = '/users/'
        factory_data = UserFactory
        response_post = self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        self.assertEqual(response_post.status_code, status.HTTP_201_CREATED)

        response = self.client.post(
            url,
            {'username': 'usernameUpde',
             'first_name': factory_data.first_name,
             'first_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_update(self):
        url = "/users/"
        factory_data = UserFactory

        self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        user = User.objects.all()[0]
        url_update = f"{url}{user.id}/"
        data = self.client.get(url_update)

        response = self.client.put(
            url_update,
            {'username': data.json()['username'],
             'first_name': "Update name",
             'last_name': "last name update",
             'email': data.json()['email'],
             'is_staff': data.json()['is_staff'],
             'password': data.json()['password']
             }
            )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], "Update name")
        self.assertEqual(response.json()['last_name'], "last name update")

    def test_update_username_empty(self):
        url = "/users/"
        factory_data = UserFactory

        self.client.post(
            url,
            {'username': factory_data.username,
             'first_name': factory_data.first_name,
             'last_name': factory_data.last_name,
             'email': factory_data.email,
             'is_staff': factory_data.is_staff,
             'password': factory_data.password
             }
        )
        user = User.objects.all()[0]
        url_update = f"{url}{user.id}/"
        data = self.client.get(url_update)
        response = self.client.put(
            url_update,
            {
                'first_name': data.json()['first_name'],
                'last_name': data.json()['last_name'],
                'email': data.json()['email'],
                'is_staff': data.json()['is_staff'],
                'password': data.json()['password']
             }
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



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

'''
