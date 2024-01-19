from core.models import Business, Product, ProductInstance
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.utils import timezone
from core.enums import CategoryChoices
from decimal import Decimal
from django.db import transaction
import uuid
from datetime import timedelta
from django.db.utils import IntegrityError


User = get_user_model()

def create_dummy_user(username='temp_user', password='password'):
    return User.objects.create_user(username=username, password=password)

def create_business(user, name="Testing Venture", description="description",
                    address="Business address", phone="0810330330", 
                    website="venture.ng", email="venture@ng.com"):
    data = {
            "user": user,
            "name": name,
            "description": description,
            "address": address,
            "phone": phone,
            "website": website,
            "email": email,
        }
    return Business.objects.create(**data)
    
def create_product(business, name='Product 001', description="Product description",
                    price=Decimal(1250), shelf_life=250, short_name=None):
    data = {
            "business": business,
            "name": name,
            "description": description,
            "price": price,
            "shelf_life": shelf_life,
            "category": CategoryChoices.CLOTHING
        }
    if short_name:
        data.update({"short_name": short_name})
    return Product.objects.create(**data)

def create_product_instance(product, manufactured=timezone.now()):
    data = {
        "product": product,
        "manufactured": manufactured
    }
    return ProductInstance.objects.create(**data)

class BusinessModelTestCase(TestCase):
    def setUp(self):
        self.user = create_dummy_user('test', 'password')
        self.business = create_business(user=self.user)
    
    def test_object_created_successfully(self):
        """test that instances are created successfully"""
        self.assertEqual(Business.objects.get(id=1), self.business)
        self.assertTrue(Business.objects.get(id=1))

    def test_str_method(self):
        """
        Test the __str__ method is correct
        """
        self.assertEqual(self.business.__str__(), "Testing Venture venture@ng.com")

    def test_no_secret(self):
        """
        Test that no secret is generated right now
        """
        self.assertEqual(self.business.secret, "")

    def test_created_get_added_automatically(self):
        """
        Test that created is auto added
        """
        self.assertTrue(self.business.created)

    def test_instance_count(self):
        """
        test that we only have one instance of Business
        """
        self.assertEqual(Business.objects.count(), 1)

    def test_unique_user_on_business(self):
        """
        Test unique constraint on user
        """
        with self.assertRaises(IntegrityError):
            create_business(user=self.user)



class ProductTestCase(TestCase):
    def setUp(self):
        self.user = create_dummy_user(username='testuser1')
        self.business = create_business(user=self.user)
        self.product = create_product(business=self.business)
    
    def test_product_created_successfully(self):
        """
        Test product created successfully
        """
        self.assertEqual(Product.objects.exists(), True)

    def test_number_of_product(self):
        """
        Test we only have one instance of product
        """
        self.assertEqual(Product.objects.count(), 1)

    def test_product_has_right_business(self):
        """
        Test the product has the right business
        """
        self.assertEqual(self.product.business, self.business)

    def test_short_name_was_auto_generated(self):
        """
        Test short name is auto generated
        """
        self.assertTrue(self.product.short_name)

    def test_unique_code_auto_generated(self):
        """
        Test unique code is auto generated
        """
        self.assertTrue(self.product.unique_code)

    def test_created_auto_added(self):
        """
        Test created is auto filled
        """
        self.assertTrue(self.product.created)

    def test_unique_product_short_name(self):
        """
        Test unique constraints on short name
        """
        short_name = self.product.short_name

        with self.assertRaises(IntegrityError):
            create_product(business=self.business, short_name=short_name)

    def test_negative_shelf_life_constraint(self):
        """
        Test using negative integer on shelf life is not valid.
        """
        with self.assertRaises(IntegrityError):
            create_product(business=self.business, shelf_life=-100)

    def test_confirm_only_one_instance_in_db(self):
        self.assertEqual(Product.objects.count(), 1)


class ProductInstanceTestCase(TestCase):
    """
    Test cases for ProductInstance model

    Args:
        TestCase (TestCase)
    """
    def setUp(self):
        self.user = create_dummy_user(username='test', password='password')
        self.business = create_business(user=self.user)
        self.product = create_product(business=self.business)
        manufactured = timezone.now()
        self.product_instance = create_product_instance(product=self.product, manufactured=manufactured)

    def test_instance_created_successfully(self):
        """
        Test that the instance was created successfully.
        """
        self.assertEqual(ProductInstance.objects.count(), 1)

    def test_id_is_uuid_field(self):
        """
        Test that the ID field is an instance of UUID
        """
        # self.assertEqual(isinstance(self.product_instance.id, uuid))
        self.assertIsInstance(self.product_instance.id, uuid.UUID)

    def test_expiry_date_was_auto_filled(self):
        """
        Test that expiry date was filled on save.
        """
        self.assertTrue(self.product_instance.expiry_date)

    
    def test_expiry_date_greater_than_manufactured_date(self):
        """
        Test that expiry date is greater than manufactured date.
        """
        message = f"{self.product_instance.expiry_date} is not greater than {self.product_instance.manufactured}"
        self.assertGreater(self.product_instance.expiry_date, self.product_instance.manufactured, message)