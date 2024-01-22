from django.test import TestCase
from account.forms import RegistrationForm
from django.contrib.auth.models import User


def create_user(username='temp', password='testpassword12', email='dummy@gmail.com'):
    return User.objects.create_user(username=username, password=password, email=email)

class RegistrationTestCase(TestCase):
    def setUp(self):
        pass

    def test_form_customization(self):
        """
        Test form fields widget customizations are correct
        """
        form = RegistrationForm()
        self.assertEqual('form-control form-control-lg', form.fields['email'].widget.attrs['class'])
        self.assertEqual('Email', form.fields['email'].widget.attrs['placeholder'])

        self.assertEqual('form-control form-control-lg', form.fields['password'].widget.attrs['class'])
        self.assertEqual('Password', form.fields['password'].widget.attrs['placeholder'])

        self.assertEqual('form-control form-control-lg', form.fields['confirm_password'].widget.attrs['class'])
        self.assertEqual('Confirm Password', form.fields['confirm_password'].widget.attrs['placeholder'])

    def test_registration_form_with_invalid_data(self):
        """
        Test that registration would not be successfull without the 3 fields
        """
        data = {}
        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.fields), len(form.errors))
        self.assertFormError(form, 'email', 'This field is required.')
        self.assertFormError(form, 'password', 'This field is required.')
        self.assertIn('This field is required.', str(form.errors.get('confirm_password')))

    def test_registration_form_with_different_password(self):
        """
        Test that form would not be valid if password and confirm_password are not the same.
        """
        data = {
            'email': 'temp@gmail.com',
            'password': 'password',
            'confirm_password': 'confirm',
        }

        form = RegistrationForm(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'password', 'Password not the same')
        self.assertFormError(form, 'confirm_password', 'Password not the same')

    def test_registration_successfull_with_valid_data(self):
        """
        Test that registration would be successfull with valid data
        """
        data = {
            'email': 'temp@gmail.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        d = form.cleaned_data
        d.pop('confirm_password')
        d.update({'username': d.get('email')})
        user = create_user(**d)
        self.assertEqual(User.objects.count(), 1)
        self.assertTrue(User.objects.get(email='temp@gmail.com'))
        self.assertTrue(user.check_password(d.get('password')))
        # form = RegistrationForm(data)
        # self.assert_

    def test_duplicate_email_not_allowed(self):
        """
        Test that user cannot register with same email more than once.
        """
        data = {
            'email': 'temp@gmail.com',
            'password': 'testpass123',
            'confirm_password': 'testpass123',
        }
        form = RegistrationForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        d = form.cleaned_data
        d.pop('confirm_password')
        d.update({'username': d.get('email')})
        create_user(**d)
        d.pop('username')
        d.update({'confirm_password': d.get('password')})
        form = RegistrationForm(d)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'email', 'User with this Email exists.')


