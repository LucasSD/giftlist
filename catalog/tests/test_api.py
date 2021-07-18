import json

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from .models import Country
from .serializers import countrieserializer

client = APIClient()

class GetAllCountriesTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # use different field combinations
        Country.objects.create(title="Country A", status=3, launch_date="2026-12-23")
        Country.objects.create(title="Country B", status=1, launch_date="2026-11-05")
        Country.objects.create(title="Country C", status=2)
        Country.objects.create(title="Country D", status=1)

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
        serializer = countryserializer(countries, many=True, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class GetSingleCountryTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # use different field combinations
        cls.CountryA = Country.objects.create(
            title="Country A", status=3, launch_date="2026-12-23"
        )
        cls.CountryB = Country.objects.create(
            title="Country B", status=1, launch_date="2026-11-05"
        )
        cls.CountryC = Country.objects.create(title="Country C", status=2)
        cls.CountryD = Country.objects.create(title="Country D", status=2)

    def test_url_exists_at_desired_location(self):
        response = self.client.get("/api/countries/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_accessible_by_name(self):
        response = self.client.get(reverse("country-detail", kwargs={"pk": self.CountryA.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_valid_single_Country(self):
        response = client.get(reverse("country-detail", kwargs={"pk": self.CountryA.pk}))
        request = response.wsgi_request
        country = Country.objects.get(pk=self.CountryA.pk)

        # context must include request due to HyperlinkedIdentityField
        serializer = countrieserializer(country, context={"request": request})
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_country(self):
        response = client.get(reverse("country-detail", kwargs={"pk": 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class CreateNewCountryTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.valid_payload = {
            "title": "Country A",
            "status": 1,
            "launch_date": "2021-12-23",
        }

        # empty title field
        cls.invalid_payload = {
            "title": "",
            "status": 2,
            "launch_date": "2021-12-23",
        }

    def test_create_valid_Country(self):
        self.assertEqual(Country.objects.count(), 0)
        response = client.post(
            reverse("Country-list"),
            data=json.dumps(self.valid_payload),
            content_type="application/json",
        )
        self.assertEqual(Country.objects.count(), 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_create_invalid_Country(self):
        self.assertEqual(Country.objects.count(), 0)
        response = client.post(
            reverse("Country-list"),
            data=json.dumps(self.invalid_payload),
            content_type="application/json",
        )
        self.assertEqual(Country.objects.count(), 0)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
