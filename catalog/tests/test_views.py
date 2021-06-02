from datetime import datetime

from django.urls import reverse
from django.test import TestCase

from catalog.models import Gift, Category, Brand, GiftInstance, Country

class CatalogIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_brand = Brand.objects.create(
            name="Apple",
            est=2001
            )

        other_brand = Brand.objects.create(
            name="Chanel",
            est=1954
            )

        Gift.objects.create(
            name="Chanel Man",
            description = "A brilliant perfume",
            ref = "randomcodeABC",
            brand = other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description = "A brilliant smartphone",
            ref = "randomcodeAZC",
            brand = test_brand,
        )

        test_gift = Gift.objects.get(id=1)
        GiftInstance.objects.create(
            gift=test_gift,
            event_date = datetime(2021, 11, 5),
            status = 't'
        )

        other_gift = Gift.objects.get(id=2)
        GiftInstance.objects.create(
            gift=other_gift,
            event_date = datetime(2021, 11, 5), # status defaults to 'a'
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_gifts"], 2)
        self.assertEqual(response.context['num_instances'], 2)
        self.assertEqual(response.context['num_instances_available'], 1)
        self.assertEqual(response.context['num_brands'], 2)
        self.assertEqual(response.context['num_perfume_gifts'], 1)
        self.assertEqual(response.context['num_older_brands'], 1)
