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
        request = response.wsgi_request
        num_visits = request.session.get('num_visits', 0)
        response = self.client.get(reverse("index"))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_gifts"], 2)
        self.assertEqual(response.context['num_instances'], 2)
        self.assertEqual(response.context['num_instances_available'], 1)
        self.assertEqual(response.context['num_brands'], 2)
        self.assertEqual(response.context['num_perfume_gifts'], 1)
        self.assertEqual(response.context['num_older_brands'], 1)
        self.assertEqual(response.context['num_visits'], 1)

class GiftListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_brand = Brand.objects.create(
            name="Apple",
            est=2001
            )

        num_gifts = 6
        for gift_id in range(num_gifts):
            Gift.objects.create(
            ref = f"ref {gift_id}",
            name=f"Iphone {gift_id}",
            brand = test_brand,
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/gifts/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("gifts"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("gifts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/gift_list.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_pagination_is_three(self):
        response = self.client.get(reverse('gifts'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['gift_list']), 3)

    def test_lists_all_gifts(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse('gifts')+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['gift_list']), 3)

    def test_context(self):
        response1 = self.client.get(reverse("gifts"))
        self.assertEqual(response1.status_code, 200)
        for i, test_gift in enumerate(response1.context['gift_list']):
            self.assertEqual(f'ref {i}', test_gift.ref)
            self.assertEqual(f"Iphone {i}", test_gift.name)
            self.assertEqual('Apple', str(test_gift.brand))
        
        response2 = self.client.get(reverse('gifts')+'?page=2')
        self.assertEqual(response2.status_code, 200)
        for j, test_gift in enumerate(response2.context['gift_list']):
            self.assertEqual(f'ref {j+3}', test_gift.ref) # adjust j for second page
            self.assertEqual(f"Iphone {j+3}", test_gift.name) # adjust j for second page
            self.assertEqual('Apple', str(test_gift.brand))

class GiftDetailViewTest(TestCase):
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
        for test_gift in Gift.objects.all():
            response = self.client.get(f"/catalog/gift/{test_gift.id}")
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for test_gift in Gift.objects.all():
            response = self.client.get(reverse("gift-detail", kwargs={"pk": test_gift.id}))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for test_gift in Gift.objects.all():
            response = self.client.get(reverse("gift-detail", kwargs={"pk": test_gift.id}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "catalog/gift_detail.html")
            self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):   
        test_gift = Gift.objects.get(id=1) 
        response = self.client.get(reverse("gift-detail", kwargs={"pk": 1}))
        self.assertEqual(test_gift.name, str(response.context['gift']))

class BrandListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_brands = 6
        for i in range(1, num_brands):
            Brand.objects.create(
            name=f"Brand {i}",
            est=1900 + i
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/brands/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("brands"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("brands"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/brand_list.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_pagination_is_two(self):
        response = self.client.get(reverse('brands'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['brand_list']), 2)

    def test_lists_all_brands(self):
        # Get third page and confirm it has (exactly) 1 remaining item
        response = self.client.get(reverse('brands')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertEqual(len(response.context['brand_list']), 1)

    def test_context(self):
        response1 = self.client.get(reverse("brands"))
        self.assertEqual(response1.status_code, 200)
        for i, test_brand in enumerate(response1.context['brand_list']):
            self.assertEqual(f"Brand {i+1}", test_brand.name)
            self.assertEqual(1900 + i+1, test_brand.est)
        
        response2 = self.client.get(reverse('brands')+'?page=3')
        self.assertEqual(response2.status_code, 200)
        test_brand = response1.context['brand_list'][0]
        #brand at end of paginator objects is in first row of database
        self.assertEqual("Brand 1", test_brand.name) 
        self.assertEqual(1901, test_brand.est)

class BrandDetailViewTest(TestCase):
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
        for test_brand in Brand.objects.all():
            response = self.client.get(f"/catalog/brand/{test_brand.id}")
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for test_brand in Brand.objects.all():
            response = self.client.get(reverse("brand-detail", kwargs={"pk": test_brand.id}))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for test_brand in Brand.objects.all():
            response = self.client.get(reverse("brand-detail", kwargs={"pk": test_brand.id}))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "catalog/brand_detail.html")
            self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):   
        test_brand = Brand.objects.get(id=1) 
        response = self.client.get(reverse("brand-detail", kwargs={"pk": 1}))
        self.assertEqual(test_brand.name, str(response.context['brand']))
