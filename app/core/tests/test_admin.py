"""
    Test for the Django Admin modifications
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client


class AdminSiteTests(TestCase):
    def setUp(self):
        """ Create user and client"""

        # Creating a client to connect to the application
        self.client = Client()

        # Creating users
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@example123',
            password='testpass123'
        )

        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='user@example123',
            password='normalUser123',
            name='TestUser'
        )

    def test_users_list(self):
        """ Test that users are listed in page """
        # With reverse and this argument we are requesting the page of Django admin where the users are listed
        # This request is made as the admin user -> admin:
        url = reverse('admin:core_user_changelist')

        # Making the HTTPreques to the url
        res = self.client.get(url)

        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_edit_user_page(self):
        """ Test that the users can be edited"""

        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """ Test the create user page works """

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
