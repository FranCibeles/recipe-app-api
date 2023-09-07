"""
    Test for the User API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

# Creating a URL Path for the user/create Endpoint
CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# Helper Function to create a user
def create_user(**params):
    """
    Create a new User
    :param params:
    :return:
    """
    return get_user_model().objects.create_user(**params)


"""
    We create public tests for unauthenticated requests (create a user)
    We create private tests for authenticated requests
"""


class PublicUserApiTests(TestCase):
    """ Tests the public features of the User API """

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        """ Test creating a new user """
        # Recreating the POST Payload for replicate the new create user action
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User'
        }

        # POST user
        res = self.client.post(CREATE_USER_URL, payload)

        # Assertions
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        # Searches the user in DB and compares the Password
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """ User with email exists """

        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test User'
        }

        # Create a User in the DB
        create_user(**payload)

        # Try to create a User through the API
        res = self.client.post(CREATE_USER_URL, payload)

        # Checking the error

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """ Checking the length of the password """

        payload = {
            'email': 'test@example.com',
            'password': 'pwd',
            'name': 'Test User'
        }

        # Try to create a User through the API
        res = self.client.post(CREATE_USER_URL, payload)

        # Assertions that we receive a BAD Request Status Code && that the user is not created at the DB
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """ Test generate token for valid credentials """

        user_details = {
            'email': 'test@example.com',
            'password': 'test-user-pass123',
            'name': 'Test User'
        }

        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """ Test returns error if credentials invalid"""

        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        """ Test that no token is created with a blank password """

        payload = {'email': 'test@example.com', 'password': ' '}

        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test authentication is required for users - Checking if an unauthorized user can retrive infos"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


class PrivateApiTests(TestCase):
    """ Test API requests that require authentication """

    def setUp(self):
        self.user = create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)


    def test_retrieve_profile_success(self):
        """ Test retrieving profile for logged in user """

        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })


    def test_post_me_not_allowed(self):
        """ Test POST is not allowed for unauthorized users """

        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


    def test_update_user_profile(self):
        """ Test updating the user profile for the authenticated users"""

        payload = {'name': 'updatedName', 'password': 'newpassword1234'}

        res = self.client.post(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['email'])
        self.assertEqual(self.user.password, payload['password'])
        self.assertEqual(res.status_code, status.HTTP_200_OK)
