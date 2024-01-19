from django.test import TestCase
from core.forms import BusinessForm, ProductForm, ProductInstanceForm
from django.http import HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username='temp', password='password'):
    return User.objects.create_user(username=username, password=password)
def get_business_form_data():

    return {
            "name": "Business Name",
            "description": "About Business",
            "address": "Location",
            "phone": "Business Hotline",
            "website": "Website URL",
            "email": "email@gmail.com"
        }

class BusinessFormTestCase(TestCase):
    """
    Tests for Business Form
    """
    def setUp(self):
        self.form = BusinessForm()
        self.request = HttpRequest()

    def test_empty_form(self):
        """
        Test the form when empty
        """
        self.assertIn("name", self.form.fields)
        self.assertIn("description", self.form.fields)
        self.assertNotIn("house", self.form.fields)
        self.assertEqual(len(self.form.fields), 6)

    def test_form_with_empty_data(self):
        data = {}
        form = BusinessForm(data)
        self.assertEqual(len(form.errors), 6)
        self.assertIn("this field is required", str(form).lower())
        self.assertFormError(form, "name", "This field is required.")
        self.assertFormError(form, "description", "This field is required.")
        self.assertFormError(form, "address", "This field is required.")
        self.assertFormError(form, "phone", "This field is required.")
        self.assertFormError(form, "website", "This field is required.")
        self.assertFormError(form, "email", "This field is required.")


    def test_form_with_invalid_data(self):
        """
        test that form raises invalid when submitted without all fields
        """
        data = get_business_form_data()
        data.pop('name')
        form = BusinessForm(data)
        self.assertTrue('This field is required.'.lower() in str(form).lower())
        self.assertFalse('Enter a valid email'.lower() in str(form).lower())
        self.assertTrue('Enter a valid URL'.lower() in str(form).lower())
        self.assertFalse(form.is_valid())

    def test_form_with_valid_data(self):
        """
        test that form is valid if all fields are provided.
        """
        data = get_business_form_data()
        data.update({"website": "website.com", "email": "email@gmail.com"})
        form = BusinessForm(data)
        self.assertTrue(form.is_valid())
