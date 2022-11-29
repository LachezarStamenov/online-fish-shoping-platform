from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

UserModel = get_user_model()


class RegisterPageTests(TestCase):
    """Registration page functionality testing"""

    def setUp(self):
        self.url = reverse('register')
        self.response = self.client.get(self.url)

    def test_register_page_exists(self):
        """Check that the page loads successfully"""
        self.assertEquals(self.response.status_code, 200)

    def test_register_template(self):
        """Check that the intended template is being used"""
        self.assertTemplateUsed(self.response, template_name='accounts/register.html')
        self.assertContains(self.response, 'register')

    def test_register_form_contains_csrf(self):
        """The form contains csrf token"""
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_register_page_submission(self):
        """Check that submission of form with valid data creates account"""
        form_details = {
            'email': 'test_user@test.com',
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '1214_tough_password1!',

        }
        user = get_user_model().objects.create_user(**form_details)
        response = self.client.post(self.url, data=form_details, follow=True)

        self.assertEqual(form_details['first_name'], user.first_name)
        self.assertEqual(form_details['last_name'], user.last_name)
        self.assertEqual(form_details['email'], user.email)
        self.assertEqual(form_details['username'], user.username)
        self.assertTrue(user.check_password(form_details['password']))

        self.assertContains(response, 'accounts/register')


class ProfilePageTests(TestCase):
    """User profile page functionality testing"""

    def setUp(self):
        url = reverse('login')
        self.response = self.client.get(url)
        self.account = {
            'email': 'test_user@test.com',
            'username': 'test_user',
            'first_name': 'Test',
            'last_name': 'User',
            'password': '225_test_password1!',
        }

        # create user account
        user = get_user_model().objects.create_user(**self.account)
        self.client.login(username=user.email)

    def test_page_not_accessible_by_public(self):
        """The page should only be accessible when the user is logged in"""
        self.assertTemplateNotUsed(
            self.response, template_name='dashboard.html')

    def test_page_accessible_when_logged_in(self):
        """The page should be accessible when the user is logged in"""
        self.client.login(email='test_user@test.com',
                          password='225_test_password1!')
        url = reverse('login')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='accounts/login.html')


