from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.test import TestCase
from django.contrib.auth import get_user_model

User = get_user_model()

# class UserModelTest(TestCase):

# 	def test_user_is_valid(self):
# 		user = User(email='ab@aol.com')
# 		user = User(username='asdfadf')
#       user = User(last_name='Yao')
# 		user = User(password='pass')
# 		user = User(first_name='Jessica')
# 		user.full_clean()
		

class AccountsTest(APITestCase):
    def setUp(self):
        # We want to go ahead and originally create a user. 
        self.test_user = User.objects.create_user('test@example.com', 'testuser', 'testpassword', 'John', 'Smith')

        # URL for creating an account.
        self.create_url = reverse('account-create')
        self.check_email = reverse('user-lookup-email')
        self.login = reverse('login')

    def test_create_user(self):
        """
        Ensure we can create a new user and a valid token is created with it.
        """
        data = {
                'email': 'foobar@example.com',
                'username': 'foobar',
                'password': 'somepassword',
                'first_name': 'john',
                'last_name': 'smith'
                }

        response = self.client.post(self.create_url , data, format='json')
        user = User.objects.latest('id')
        token = Token.objects.get(user=user)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['email'], data['email'])
        self.assertEqual(response.data['token'], token.key)
        self.assertFalse('password' in response.data)


    def test_create_user_with_short_password(self):
        """
        Ensures user is not created for password lengths less than 8.
        """

        data = {
                'email': 'foobarbaz@example.com',
                'username': 'foobar',
                'password': 'foo',
                'first_name': 'john',
                'last_name': 'smith'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_no_password(self):
        data = {
                'email': 'foobarbaz@example.com',
                'username': 'foobar',
                'password': '',
                'first_name': 'john',
                'last_name': 'smith'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['password']), 1)

    def test_create_user_with_too_long_username(self):
        data = {
            'email': 'foobarbaz@example.com',
            'username': 'foo'*30,
            'password': 'foobar',
            'first_name': 'john',
            'last_name': 'smith'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)
    
    def test_create_user_with_no_username(self):
        data = {
                'email': 'foobarbaz@example.com',
                'username': '',
                'password': 'foobarbaz',
                'first_name': 'john',
                'last_name': 'smith'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_username(self):
        data = {
                'email': 'user@example.com',
                'username': 'testuser',
                'password': 'testuser',
                'first_name': 'john',
                'last_name': 'smith'
                }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['username']), 1)

    def test_create_user_with_preexisting_email(self):
        data = {
            'email': 'test@example.com',
            'username': 'testuser2',
            'password': 'testuser',
            'first_name': 'john',
            'last_name': 'smith'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)


    def test_create_user_with_invalid_email(self):
        data = {
            'email':  'testing',
            'username': 'foobarbaz',
            'passsword': 'foobarbaz',
            'first_name': 'john',
            'last_name': 'smith'
        }


        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)
    
    def test_create_user_with_no_email(self):
        data = {
                'email': '',
                'username' : 'foobar',
                'password': 'foobarbaz',
                'first_name': 'john',
                'last_name': 'smith'
        }

        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(len(response.data['email']), 1)
    
    def test_check_email_unique(self):
        data = {
                'email': 'unique@aol.com',
                'username' : 'foobar',
                'password': 'foobarbaz',
                'first_name': 'john',
                'last_name': 'smith'
        }

        response = self.client.get(self.check_email, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(User.objects.count(), 1)

    def test_check_email_not_unique(self):
        data = {
                'email': 'test@example.com',
                'username' : 'foobar1',
                'password': 'foobarbaz123',
                'first_name': 'john',
                'last_name': 'smith'
        }

        response = self.client.get(self.check_email, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_check_email_login_wrong_password(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpassword1'
        }
        response = self.client.post(self.login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)
    
    def test_check_email_login_correct_password(self):
        data = {
            'username': 'test@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

    def test_check_username_login_wrong_password(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword1'
        }
        response = self.client.post(self.login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)
    
    def test_check_username_login_correct_password(self):
        data = {
            'username': 'testuser',
            'password': 'testpassword'
        }
        response = self.client.post(self.login, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)
