from django.test import TestCase
from core.forms import BusinessForm, ProductForm, ProductInstanceForm
from django.http import HttpRequest
from django.contrib.auth import get_user_model

User = get_user_model()

def create_user(username='temp', password='password'):
    return User.objects.create_user(username=username, password=password)

BUSINESS_FORM_DATA = {
            "name": "Business Name",
            "description": "About Business",
            "address": "Location",
            "phone": "Business Hotline",
            "website": "Website URL",
            "email": "Business Email"
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

    def test_form_with_invalid_data(self):
        """
        test that form raises invalid when submitted without all fields
        """
        data = BUSINESS_FORM_DATA
        data.pop("email")
        data.pop('name')
        form = self.form(data)
        print('form: ', form)
        self.assertInHTML('This field is required', str(form))

