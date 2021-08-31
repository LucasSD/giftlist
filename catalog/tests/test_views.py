from datetime import datetime

from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from catalog.models import Gift, Category, Brand, GiftInstance, Country


class CatalogIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)

        other_brand = Brand.objects.create(name="Chanel", est=1954)

        Gift.objects.create(
            name="Chanel Man",
            description="A brilliant perfume",
            ref="randomcodeABC",
            brand=other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeAZC",
            brand=test_brand,
        )

        test_gift = Gift.objects.get(id=1)
        GiftInstance.objects.create(
            gift=test_gift, event_date=datetime(2021, 11, 5), status="t"
        )

        other_gift = Gift.objects.get(id=2)
        GiftInstance.objects.create(
            gift=other_gift,
            event_date=datetime(2021, 11, 5),  # status defaults to 'a'
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
        num_visits = request.session.get("num_visits", 0)
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["num_gifts"], 2)
        self.assertEqual(response.context["num_instances"], 2)
        self.assertEqual(response.context["num_instances_available"], 1)
        self.assertEqual(response.context["num_brands"], 2)
        self.assertEqual(response.context["num_perfume_gifts"], 1)
        self.assertEqual(response.context["num_older_brands"], 1)
        self.assertEqual(response.context["num_visits"], 1)


class GiftListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):

        test_brand = Brand.objects.create(name="Apple", est=2001)

        num_gifts = 6
        for gift_id in range(num_gifts):
            Gift.objects.create(
                ref=f"ref {gift_id}",
                name=f"Iphone {gift_id}",
                brand=test_brand,
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
        response = self.client.get(reverse("gifts"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["gift_list"]), 3)

    def test_lists_all_gifts(self):
        # Get second page and confirm it has (exactly) remaining 3 items
        response = self.client.get(reverse("gifts") + "?page=2")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["gift_list"]), 3)

    def test_context(self):
        response1 = self.client.get(reverse("gifts"))
        self.assertEqual(response1.status_code, 200)
        for i, test_gift in enumerate(response1.context["gift_list"]):
            self.assertEqual(f"ref {i}", test_gift.ref)
            self.assertEqual(f"Iphone {i}", test_gift.name)
            self.assertEqual("Apple", str(test_gift.brand))

        response2 = self.client.get(reverse("gifts") + "?page=2")
        self.assertEqual(response2.status_code, 200)
        for j, test_gift in enumerate(response2.context["gift_list"]):
            self.assertEqual(f"ref {j + 3}", test_gift.ref)  # adjust j for second page
            self.assertEqual(
                f"Iphone {j + 3}", test_gift.name
            )  # adjust j for second page
            self.assertEqual("Apple", str(test_gift.brand))


class GiftDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)

        other_brand = Brand.objects.create(name="Chanel", est=1954)

        Gift.objects.create(
            name="Chanel Man",
            description="A brilliant perfume",
            ref="randomcodeABC",
            brand=other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeAZC",
            brand=test_brand,
        )

        test_gift = Gift.objects.get(id=1)
        GiftInstance.objects.create(
            gift=test_gift, event_date=datetime(2021, 11, 5), status="t"
        )

        other_gift = Gift.objects.get(id=2)
        GiftInstance.objects.create(
            gift=other_gift,
            event_date=datetime(2021, 11, 5),  # status defaults to 'a'
        )

    def test_view_url_exists_at_desired_location(self):
        for test_gift in Gift.objects.all():
            response = self.client.get(f"/catalog/gift/{test_gift.id}")
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for test_gift in Gift.objects.all():
            response = self.client.get(
                reverse("gift-detail", kwargs={"pk": test_gift.id})
            )
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for test_gift in Gift.objects.all():
            response = self.client.get(
                reverse("gift-detail", kwargs={"pk": test_gift.id})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "catalog/gift_detail.html")
            self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):
        test_gift = Gift.objects.get(id=1)
        response = self.client.get(reverse("gift-detail", kwargs={"pk": 1}))
        self.assertEqual(test_gift.name, str(response.context["gift"]))


# need to add pagination tests
class GiftInstanceListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)

        num_gifts = 6
        for gift_id in range(num_gifts):
            Gift.objects.create(
                ref=f"ref {gift_id}",
                name=f"Iphone {gift_id}",
                brand=test_brand,
            )

        test_requester1 = User.objects.create(username="johnsmith", password="password")
        test_requester2 = User.objects.create(
            username="davidjones", password="password"
        )

        # may be redundant
        test_gift1 = Gift.objects.get(id=1)
        test_gift2 = Gift.objects.get(id=2)

        # may be redundant
        test_giftinstance1 = GiftInstance.objects.create(
            gift=test_gift1, requester=test_requester1
        )
        test_giftinstance2 = GiftInstance.objects.create(
            gift=test_gift2, requester=test_requester2
        )

    def setUp(self):
        self.client.force_login(User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("mygifts"))
        self.assertRedirects(response, "/accounts/login/?next=/catalog/mygifts/")

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get("/catalog/mygifts/")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("mygifts"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("mygifts"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/giftinstance_list.html")
        self.assertTemplateUsed(response, "base_generic.html")

    # TODO: fully understand and improve below
    def test_context(self):
        response = self.client.get(reverse("mygifts"))
        self.assertEqual(response.status_code, 200)
        test_giftinstance = response.context["giftinstance_list"][0]
        self.assertEqual(f"ref 0", test_giftinstance.gift.ref)
        self.assertEqual(f"Iphone 0", test_giftinstance.gift.name)
        self.assertEqual("Apple", str(test_giftinstance.gift.brand))
        self.assertEqual("johnsmith", str(test_giftinstance.requester))

    def test_displays_logged_in_user_only(self):
        response = self.client.get(reverse("mygifts"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(response.context["giftinstance_list"]))


class GiftInstanceCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)
        other_brand = Brand.objects.create(name="Chanel", est=1954)

        Gift.objects.create(
            name="Chanel Man",
            description="A brilliant perfume",
            ref="randomcodeABC",
            brand=other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeAZC",
            brand=test_brand,
        )

        test_requester = User.objects.create(username="johnsmith", password="password")

        test_gift = Gift.objects.get(id=1)
        other_gift = Gift.objects.get(id=2)

        form_entry = {
            "gift": test_gift,
            "event_date": "25/12/2021",
            "size": "200ml",
            "colour": "NA",
            "price": "£90",
            "url": "www.chanel.com",
            "requester": test_requester,
            "status": "a",
        }

    def setUp(self):
        self.client.force_login(user=User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        response = self.client.get(reverse("giftinstance-create"))
        self.assertRedirects(
            response, f"/accounts/login/?next=/catalog/mygift/create"
        )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get(f"/catalog/mygift/create")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse("giftinstance-create"))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse("giftinstance-create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/giftinstance_form.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_initial_form_context(self):
        response = self.client.get(reverse("giftinstance-create"))
        self.assertEqual(response.status_code, 200)
        test_form = response.context["form"]
        self.assertIn("form", response.context)
        self.assertEqual({}, test_form.initial)

    def test_form_post(self):
        self.assertEqual(GiftInstance.objects.count(), 0)
        response = self.client.post(reverse("giftinstance-create"), data=self.form_entry)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(GiftInstance.objects.count(), 1)

        test_giftinstance = GiftInstance.objects.get(id=1)
        self.assertEqual("200ml", test_giftinstance.size)
        self.assertEqual("johnsmith", str(test_giftinstance.requester))
        self.assertEqual("Chanel Man", test_giftinstance.gift)

    def test_form_post_invalid(self):
        # empty form
        invalid_form_entry = {
        }

        response = self.client.post(reverse("giftinstance-create"), data=invalid_form_entry)
        self.assertEqual(response.status_code, 200)

        # check nothing added to database
        self.assertEqual(GiftInstance.objects.count(), 0)

class GiftInstanceUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)

        other_brand = Brand.objects.create(name="Chanel", est=1954)

        Gift.objects.create(
            name="Chanel Man",
            description="A brilliant perfume",
            ref="randomcodeABC",
            brand=other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeAZC",
            brand=test_brand,
        )

        test_requester = User.objects.create(username="johnsmith", password="password")

        test_gift = Gift.objects.get(id=1)
        GiftInstance.objects.create(
            gift=test_gift,
            event_date=datetime(2021, 11, 5),
            status="t",
            requester=test_requester,
        )

        other_gift = Gift.objects.get(id=2)
        GiftInstance.objects.create(
            gift=other_gift,
            event_date=datetime(2021, 11, 5),  # status defaults to 'a'
            requester=test_requester,
        )

    def setUp(self):
        self.client.force_login(user=User.objects.get(id=1))

    def test_redirect_if_not_logged_in(self):
        self.client.logout()
        test_giftinstance = GiftInstance.objects.all()[0]
        response = self.client.get(
            reverse("giftinstance-update", kwargs={"pk": test_giftinstance.id})
        )
        self.assertRedirects(
            response, f"/accounts/login/?next=/catalog/mygift/{test_giftinstance.id}"
        )

    def test_view_url_exists_at_desired_location(self):
        test_giftinstance = GiftInstance.objects.all()[0]
        response = self.client.get(f"/catalog/mygift/{test_giftinstance.id}")
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        test_giftinstance = GiftInstance.objects.all()[0]
        response = self.client.get(
            reverse("giftinstance-update", kwargs={"pk": test_giftinstance.id})
        )
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        test_giftinstance = GiftInstance.objects.all()[0]
        response = self.client.get(
            reverse("giftinstance-update", kwargs={"pk": test_giftinstance.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "catalog/giftinstance_form.html")
        self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):
        # get object by status for tests. UUID as pk is not necessary but removing
        # UUID field causes migration problems
        test_giftinstance = GiftInstance.objects.get(status="t")
        response = self.client.get(
            reverse("giftinstance-update", kwargs={"pk": test_giftinstance.id})
        )
        self.assertIn("Chanel", str(response.context["giftinstance"]))
        self.assertIn("form", response.context)


class BrandListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        num_brands = 6
        for i in range(1, num_brands):
            Brand.objects.create(name=f"Brand {i}", est=1900 + i)

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
        response = self.client.get(reverse("brands"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["brand_list"]), 2)

    def test_lists_all_brands(self):
        # Get third page and confirm it has (exactly) 1 remaining item
        response = self.client.get(reverse("brands") + "?page=3")
        self.assertEqual(response.status_code, 200)
        self.assertTrue("is_paginated" in response.context)
        self.assertTrue(response.context["is_paginated"] == True)
        self.assertEqual(len(response.context["brand_list"]), 1)

    def test_context(self):
        response1 = self.client.get(reverse("brands"))
        self.assertEqual(response1.status_code, 200)
        for i, test_brand in enumerate(response1.context["brand_list"]):
            self.assertEqual(f"Brand {i + 1}", test_brand.name)
            self.assertEqual(1900 + i + 1, test_brand.est)

        response2 = self.client.get(reverse("brands") + "?page=3")
        self.assertEqual(response2.status_code, 200)
        test_brand = response1.context["brand_list"][0]
        # brand at end of paginator objects is in first row of database
        self.assertEqual("Brand 1", test_brand.name)
        self.assertEqual(1901, test_brand.est)


class BrandDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_brand = Brand.objects.create(name="Apple", est=2001)

        other_brand = Brand.objects.create(name="Chanel", est=1954)

        Gift.objects.create(
            name="Chanel Man",
            description="A brilliant perfume",
            ref="randomcodeABC",
            brand=other_brand,
        )

        Gift.objects.create(
            name="Iphone 11",
            description="A brilliant smartphone",
            ref="randomcodeAZC",
            brand=test_brand,
        )

        test_gift = Gift.objects.get(id=1)
        GiftInstance.objects.create(
            gift=test_gift, event_date=datetime(2021, 11, 5), status="t"
        )

        other_gift = Gift.objects.get(id=2)
        GiftInstance.objects.create(
            gift=other_gift,
            event_date=datetime(2021, 11, 5),  # status defaults to 'a'
        )

    def test_view_url_exists_at_desired_location(self):
        for test_brand in Brand.objects.all():
            response = self.client.get(f"/catalog/brand/{test_brand.id}")
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for test_brand in Brand.objects.all():
            response = self.client.get(
                reverse("brand-detail", kwargs={"pk": test_brand.id})
            )
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for test_brand in Brand.objects.all():
            response = self.client.get(
                reverse("brand-detail", kwargs={"pk": test_brand.id})
            )
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, "catalog/brand_detail.html")
            self.assertTemplateUsed(response, "base_generic.html")

    def test_context(self):
        test_brand = Brand.objects.get(id=1)
        response = self.client.get(reverse("brand-detail", kwargs={"pk": 1}))
        self.assertEqual(test_brand.name, str(response.context["brand"]))
