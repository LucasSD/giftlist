import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from catalog.models import Country
from giftapi.serializers import CountrySerializer

client = APIClient()

class GetAllCountriesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        Country.objects.create(name="Country A")
        Country.objects.create(name="Country B")
        Country.objects.create(name="Country C")
        Country.objects.create(name="Country D")

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
