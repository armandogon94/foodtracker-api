from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch

from core import models


def sample_user(public_name='name',
                email='test@gmail.com',
                password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(public_name, email, password)


class ModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        public_name = 'nombre'
        email = 'hola@gmail.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            public_name=public_name,
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertEqual(user.public_name, public_name)
        # We use asserTrue because password is encrypted
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        public_name = 'test1'
        email = 'test@GMAIL.COM'
        user = get_user_model().objects.create_user(
            public_name,
            email,
            'test123'
        )

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('name1', None, 'test123')

    def test_new_user_invalid_username(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                None,
                'test@test.com',
                'test123'
            )

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'testsuperuser',
            'test@gmail.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
