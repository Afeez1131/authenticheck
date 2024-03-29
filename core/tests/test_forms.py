from django.test import TestCase
from core.forms import BusinessForm, ProductForm, ProductInstanceForm
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from core.models import Business, Product, ProductInstance
from .test_models import create_business, create_product
from decimal import Decimal
from core.enums import CategoryChoices
from django.utils import timezone
from datetime import timedelta


User = get_user_model()

def create_user(username='temp', password='password'):
    return User.objects.create_user(username=username, password=password)


def get_business_form_data():
    user = create_user()
    return {
            # "user": user.id,
            "name": "Business Name",
            "description": "About Business",
            "address": "Location",
            "phone": "Business Hotline",
            "website": "Website URL",
            "email": "email@gmail.com"
        }

def get_product_data():
    return {
            "name": "Product Name",
            "description": "Product Description",
            "price": Decimal(1250),
            "shelf_life": 250,
            "category": CategoryChoices.CLOTHING
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
        user = create_user(username='testing1')
        form = BusinessForm(data)
        form.instance.user = user
        self.assertEqual(Business.objects.count(), 0)
        form.save()
        self.assertEqual(Business.objects.count(), 1)
        self.assertTrue(form.is_valid())

    def test_field_customization(self):
        """
        Test that widget customization is effected on the fields
        """
        form = BusinessForm()
        self.assertIn('class="form-control"', str(form['name']))
        self.assertIn('placeholder="Business Name', str(form['name']))

        self.assertIn('class="form-control"', str(form['description']))
        self.assertIn('placeholder="Business Description"', str(form['description']))

        self.assertIn('class="form-control"', str(form['address']))
        self.assertIn('placeholder="Business Address"', str(form['address']))

        self.assertIn('class="form-control"', str(form['phone']))
        self.assertIn('placeholder="Business Phone"', str(form['phone']))

        self.assertIn('class="form-control"', str(form['website']))
        self.assertIn('placeholder="Business Website"', str(form['website']))

        self.assertIn('class="form-control"', str(form['email']))
        self.assertIn('placeholder="Business E-mail"', str(form['email']))

    def test_widget_customization(self):
        """
        Test that widget customizations is effected
        """
        form = BusinessForm()
        self.assertEqual('Business Name', form.fields['name'].label)
        self.assertEqual('form-control', form.fields['name'].widget.attrs['class'])

        self.assertEqual('About Business', form.fields['description'].label)
        self.assertEqual('form-control', form.fields['description'].widget.attrs['class'])

        self.assertEqual('Location', form.fields['address'].label)
        self.assertEqual('form-control', form.fields['address'].widget.attrs['class'])

        self.assertEqual('Website URL', form.fields['website'].label)
        self.assertEqual('form-control', form.fields['website'].widget.attrs['class'])
        # print(form.fields.get("email").label)
        self.assertEqual('Business Email', form.fields['email'].label)
        self.assertEqual('form-control', form.fields['email'].widget.attrs['class'])


class ProductFormTestCase(TestCase):
    """
    Tests for Product Form
    """
    def test_form_with_empty_data(self):
        """
        Test that form submitted with empty data would be invalid
        """
        data = {}
        form = ProductForm(data)
        form.is_valid()
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), len(form.fields))
        self.assertFormError(form, 'name', 'This field is required.')
        self.assertFormError(form, 'description', 'This field is required.')
        self.assertEqual(len(form.errors.get("price")), 2)
        self.assertIn("This field is required.", form.errors.get("price"))
        self.assertIn("Invalid Price ", form.errors.get("price"))

        self.assertEqual(len(form.errors.get("shelf_life")), 2)
        self.assertIn("This field is required.", form.errors.get("shelf_life"))
        self.assertIn("Invalid Shelf Life ", form.errors.get("shelf_life"))
        self.assertFormError(form, 'category', 'This field is required.')


    def test_form_get_submitted_with_valid_data(self):
        """
        Test that form would submit successfully with valid data.
        """
        user = create_user(username='hello')
        business = create_business(user=user)
        data = get_product_data()
        form = ProductForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(Product.objects.count(), 0)
        form.instance.business = business
        form.save()
        self.assertEqual(Product.objects.count(), 1)

    def test_field_customization(self):
        """
        Test that widget customization are effected on the fields
        """
        form = ProductForm()
        self.assertIn('class="form-control', str(form['name']))
        self.assertIn('placeholder="Product Name', str(form['name']))

        self.assertIn('class="form-control"', str(form['description']))
        self.assertIn('placeholder="Product Description"', str(form['description']))

        self.assertIn('class="form-control"', str(form['price']))
        self.assertIn('placeholder="Product Price"', str(form['price']))

        self.assertIn('class="form-control"', str(form['shelf_life']))
        self.assertIn('placeholder="Product Expected Shelf Life"', str(form['shelf_life']))

        self.assertIn('class="select2 w-100"', str(form['category']))

    def test_widget_customization(self):
        """
        Test that widget customizations are effected
        """
        form = ProductForm()
        self.assertEqual('Product Name', form.fields['name'].label)
        self.assertEqual('Product Description', form.fields['description'].label)
        self.assertEqual('Price of Product', form.fields['price'].label)
        self.assertEqual('Shelf Life of Product', form.fields['shelf_life'].label)
        self.assertEqual('Product Category', form.fields['category'].label)

        self.assertEqual('form-control', form.fields['name'].widget.attrs['class'])
        self.assertEqual('form-control', form.fields['description'].widget.attrs['class'])
        self.assertEqual('form-control', form.fields['description'].widget.attrs['class'])
        self.assertEqual('form-control', form.fields['shelf_life'].widget.attrs['class'])
        self.assertEqual('select2 w-100', form.fields['category'].widget.attrs['class'])


class TestProductInstanceForm(TestCase):
    """
    Tests for the Product Instance form
    """
    def test_form_is_invalid_with_empty_data(self):
        data = {}
        form = ProductInstanceForm(data)
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), len(form.fields))
        self.assertFormError(form, 'product', "This field is required.")
        self.assertIn('This field is required.', form.errors.get("manufactured"))
        

    def test_form_with_valid_data(self):
        """
        Test that form is saved correctly with valid data
        """
        user = create_user(username='heye')
        business = create_business(user=user)
        product = create_product(business=business, name='Tomato')
        data = {
            "product": product,
            "manufactured": timezone.now()
        }
        form = ProductInstanceForm(data)
        self.assertTrue(form.is_valid())
        self.assertEqual(len(form.errors), 0)
        self.assertEqual(ProductInstance.objects.count(), 0)
        p = form.save()
        self.assertEqual(ProductInstance.objects.count(), 1)
        self.assertEqual(p.product.name, 'Tomato')
        self.assertGreater(p.expiry_date, p.manufactured)

    def test_form_with_past_and_future_manufactured_date(self):
        """
        Test that test would fail if manufactured date is not today
        """
        user = create_user(username='world')
        business = create_business(user=user)
        product = create_product(business=business, name='Titus')
        data = {
            "product": product,
            "manufactured": timezone.now() + timedelta(days=2)
        }
        form = ProductInstanceForm(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'manufactured', 'Manufactured date should be the same as today.')
        data.update({"manufactured": timezone.now() - timedelta(days=5)})
        form = ProductInstanceForm(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'manufactured', "Manufactured date should be the same as today.")

    def test_form_without_product(self):
        """
        Test that form would fail without product
        """
        data = {
            "manufactured": timezone.now() + timedelta(days=2)
        }
        form = ProductInstanceForm(data)
        self.assertFalse(form.is_valid())
        self.assertFormError(form, 'product', 'This field is required.')

    def test_model_is_populated_with_instance_data(self):
        user = create_user(username='world')
        business = create_business(user=user)
        product = create_product(business=business, name='Titus2')
        now = timezone.now()
        data = {
            "product": product,
            "manufactured": now
        }
        f = ProductInstanceForm(data)
        product_instance = f.save()
        form = ProductInstanceForm(instance=product_instance)
        self.assertEqual(form['product'].value(), product.id)
        self.assertEqual(product_instance.manufactured, now)

    def test_field_customization(self):
        """
        Test that widgets are used on the fields as specified.
        """
        form = ProductInstanceForm()
        self.assertIn('class="form-control"', str(form))
        self.assertIn('class="form-select"', str(form['product']))
        self.assertIn('class="form-control"', str(form['manufactured']))

    def test_widget_customization(self):
        """
        Test that widget customizations are eeffected
        """
        form = ProductInstanceForm()
        self.assertEqual('Product', form.fields['product'].label)
        self.assertEqual('Manufactured Date', form.fields['manufactured'].label)

        self.assertEqual('form-select', form.fields['product'].widget.attrs['class'])
        self.assertEqual('form-control', form.fields['manufactured'].widget.attrs['class'])
