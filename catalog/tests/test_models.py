
from datetime import datetime

from django.test import TestCase

from catalog.models import Gift, Category, Brand, GiftInstance

class CategoryModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        Category.objects.create(name="Perfume")

    def test_name_max_length(self):
        test_category = Category.objects.get(id=1)
        max_length = test_category._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_category_name(self):  # test __str__
        test_category = Category.objects.get(id=1)
        expected_object_name = f"{test_category.name}"
        self.assertEqual(expected_object_name, str(test_category))

class GiftModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods

        test_category = Category.objects.create(name="Mobile Phone")
        test_country = Country.objects.create(name="USA")
        test_brand = Brand.objects.create(
            name="Apple",
            est=datetime.date(1976)
            )

        test_gift = Gift.objects.create(
            name="Iphone 11",
            description = "A brilliant smartphone",
            ref = "randomcodeABC",
            price = 1000.00,
            url = "https://www.apple.com/uk/shop/buy-iphone/iphone-11",
            brand = test_brand,
            made_in = test_country,
        )

    def test_name_max_length(self):
        test_gift = Gift.objects.get(id=1)
        max_length = test_gift._meta.get_field("name").max_length
        self.assertEqual(max_length, 200)

    def test_category_field(self):
        test_category = Category.objects.get(id=1)
        test_category.save()

        test_gift = Gift.objects.get(id=1)
        test_gift.category.add(test_category)
        test_gift.save()
        expected_category = str(
            test_gift.category.all()[0]
        )  # queryset is a list of length one
        self.assertEqual(expected_category, "Mobile Phone")

    def test_brand_field(self):  # test ForeignKey Field
        test_gift = Gift.objects.get(id=1)
        expected_brand = test_gift.brand
        self.assertEqual(str(expected_brand), "Apple")

    def test_description_max_length(self):
        test_gift = Gift.objects.get(id=1)
        max_length = test_gift._meta.get_field("description").max_length
        self.assertEqual(max_length, 1000)

    def test_description_help_text(self):
        test_gift = Gift.objects.get(id=1)
        help_text = test_gift._meta.get_field("description").help_text
        self.assertEqual(help_text, "Enter a brief description of the gift")

    def test_ref_max_length(self):
        test_gift = Gift.objects.get(id=1)
        max_length = test_gift._meta.get_field("ref").max_length
        self.assertEqual(max_length, 20)
    
    def test_ref_help_text(self):
        test_gift = Gift.objects.get(id=1)
        help_text = test_gift._meta.get_field("ref").help_text
        self.assertEqual(help_text, "Enter a product code or similar as a reference")

    def test_made_in(self):  # test ForeignKey Field
        test_gift = Gift.objects.get(id=1)
        expected_country = test_gift.made_in
        self.assertEqual(str(expected_country), "USA")

    def test_price_max_digits(self):
        test_gift = Gift.objects.get(id=1)
        expected_max_digits = test_gift._meta.get_field("price").max_digits
        self.assertEqual(expected_max_digits, 10)

    def test_price_decimal_places(self):
        test_gift = Gift.objects.get(id=1)
        expected_decimal_places = test_gift._meta.get_field("price").decimal_places
        self.assertEqual(expected_decimal_places, 10)

    def test_object_name_is_gift_name(self):  # test __str__
        test_gift = Gift.objects.get(id=1)
        expected_object_name = f"{test_gift.name}"
        self.assertEqual(expected_object_name, str(test_gift))

    def test_get_absolute_url(self):
        test_gift = Gift.objects.get(id=1)
        # This will also fail if the urlconf is not defined.
        self.assertEqual(test_gift.get_absolute_url(), '/catalog/gift/1')

