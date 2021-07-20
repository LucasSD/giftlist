import json

from catalog.models import Brand, Category, Country, Gift
from django.urls import reverse
from giftapi.serializers import (BrandSerializer, CategorySerializer,
                                 CountrySerializer)
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

client = APIClient()

class GetAllCountriesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name="Country D")
        Country.objects.create(name="Country C")
        Country.objects.create(name="Country A")
        Country.objects.create(name="Country B")

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/countries/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("country-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_countries(self):

        response = self.client.get(reverse("country-list"))

        countries = Country.objects.all()
        request = response.wsgi_request

        # context must include request due to HyperlinkedIdentityField
        serializer = CountrySerializer(countries, many=True, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_by_name(self):
        response = self.client.get(reverse("country-list"))
        self.assertEqual(response.data[0]["name"], "Country A")
        self.assertEqual(response.data[2]["name"], "Country C")



class CreateNewCountryTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_payload = {
            "name": "Country A",
        }

        
        cls.invalid_payload = {
        }

    def test_create_valid_country(self):
        self.assertEqual(Country.objects.count(), 0)
        response = client.post(
            reverse("country-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_country(self):
        self.assertEqual(Country.objects.count(), 0)
        response = client.post(
            reverse("country-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetAllCategoriesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Category.objects.create(name="Dinner Sets")
        Category.objects.create(name="Cricket")
        Category.objects.create(name="Astrology")
        Category.objects.create(name="Books")

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/categories/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_categories(self):

        response = self.client.get(reverse("category-list"))

        categories = Category.objects.all()
        request = response.wsgi_request

        # context must include request due to HyperlinkedIdentityField
        serializer = CategorySerializer(categories, many=True, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_by_name(self):
        response = self.client.get(reverse("category-list"))
        self.assertEqual(response.data[0]["name"], "Astrology")
        self.assertEqual(response.data[2]["name"], "Cricket")



class CreateNewCategoryTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_payload = {
            "name": "Astrology",
        }

        
        cls.invalid_payload = {
        }

    def test_create_valid_category(self):
        self.assertEqual(Category.objects.count(), 0)
        response = client.post(
            reverse("category-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_category(self):
        self.assertEqual(Category.objects.count(), 0)
        response = client.post(
            reverse("category-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(Category.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetAllBrandsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # use different field combinations
        Brand.objects.create(name="Brand D", est=1984)
        Brand.objects.create(name="Brand A", est=1950)
        Brand.objects.create(name="Brand B")
        Brand.objects.create(name="Brand C")

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/brands/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("brand-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_brands(self):
        response = self.client.get(reverse("brand-list"))
        brands = Brand.objects.all()
        request = response.wsgi_request

        serializer = BrandSerializer(brands, many=True, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ordering_by_name(self):
        response = self.client.get(reverse("brand-list"))
        self.assertEqual(response.data[0]["name"], "Brand A")
        self.assertEqual(response.data[2]["name"], "Brand C")

class CreateNewBrandTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_payload = {
            "name": "brand A",
            "est": 1984
        }

        # est not integer
        cls.invalid_payload = {
            "name": "Brand B",
            "est" : "bad data"

        }

    def test_create_valid_brand(self):
        self.assertEqual(Brand.objects.count(), 0)
        response = client.post(
            reverse("brand-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(Brand.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_brand(self):
        self.assertEqual(Brand.objects.count(), 0)
        response = client.post(
            reverse("brand-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(Brand.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class GetAllGiftsTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # use different field combinations
        test_category = Category.objects.create(name="Mobile Phone")
        test_country = Country.objects.create(name="USA")
        test_brand = Brand.objects.create(name="Apple", est=1976)

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeABC",
            brand=test_brand,
            made_in=test_country,
        )

        Gift.objects.create(
            name="Iphone 15",
            description="An even better smartphone",
            ref="randomcodeXYZ",
            brand=test_brand,
            made_in=test_country,
        )

        Gift.objects.create(
            name="MacBook",
            description="A nice laptop",
            ref="randomcodeHIJ",
            brand=test_brand,
            made_in=test_country,
        )

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/gifts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("gift-list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_all_gifts(self):
        response = self.client.get(reverse("gift-list"))
        gifts = Gift.objects.all()
        request = response.wsgi_request

        serializer = GiftSerializer(gifts, many=True, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class CreateNewGiftTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        test_country = Country.objects.create(name="USA")
        test_brand = Brand.objects.create(name="Apple", est=1976)
        
        cls.valid_payload = {
            "name": "MacBook",
            "description": "A nice laptop",
            "ref": "randomcodeHIJ",
            "brand": test_brand,
            "made_in": test_country,
        }

        # blank name field
        cls.invalid_payload = {
            "name": "",
            "description": "A nice laptop",
            "ref": "randomcodeHIJ",
            "brand": test_brand,
            "made_in": test_country,
        }

    def test_create_valid_gift(self):
        self.assertEqual(Gift.objects.count(), 0)
        response = client.post(
            reverse("gift-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(Gift.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_gift(self):
        self.assertEqual(Gift.objects.count(), 0)
        response = client.post(
            reverse("gift-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(Gift.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



 

