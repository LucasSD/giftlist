import uuid  # Required for unique gift instances
from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Category(models.Model):
    """Model representing a gift category."""

    name = models.CharField(
        max_length=200, help_text="Enter a gift category (e.g. electronics or clothes)",
        unique = True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        """String for representing the Model object."""
        return self.name


class Gift(models.Model):
    """Model representing a Gift (but not a gift instance which is more specific and which a user has requested)."""

    name = models.CharField(max_length=200)

    brand = models.ForeignKey("Brand", on_delete=models.RESTRICT, null=True)
    description = models.TextField(
        max_length=1000, help_text="Enter a brief description of the gift"
    )
    ref = models.CharField(
        max_length=20,
        unique=True,
        help_text="Enter a product code or similar as a reference",
    )

    category = models.ManyToManyField(
        Category, help_text="Select a category for this gift",
        blank=True
    )

    made_in = models.ForeignKey("Country", on_delete=models.RESTRICT, null=True)

    class Meta:
        ordering = [
            "id"
        ]  # this orders the database and avoids ordering warnings related to pagination

    def display_category(self):
        """Create a string for the Category. This is required to display categories in Admin."""
        return ", ".join(category.name for category in self.category.all()[:3])

    display_category.short_description = "Category"

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this gift."""
        return reverse("gift-detail", args=[str(self.id)])


class GiftInstance(models.Model):
    """Model representing a specific size or colour of a gift that appear on lists (i.e. that can be taken by a buyer)."""

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        help_text="Unique ID for this specific gift requested by a single user",
    )
    gift = models.ForeignKey("Gift", on_delete=models.RESTRICT, null=True)
    event_date = models.DateField(null=True, blank=True)
    size = models.TextField(
        max_length=1000,
        default="",
        help_text="Enter notes regarding what size you need",
    )
    colour = models.CharField(
        max_length=400,
        default="",
        help_text="Enter notes regarding what colour you want",
    )
    price = models.DecimalField(max_digits=10, default=0.00, decimal_places=2)
    url = models.URLField(
        default="", help_text="enter a link which might help your buyer"
    )

    # on_delete setting may change between dev and production
    requester = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )

    @property
    def is_expired(self):
        if date.today() > self.event_date:
            return True
        return False

    AVAILABLE_STATUS = (
        ("a", "Available"),
        ("t", "Taken"),
    )

    status = models.CharField(
        max_length=1,
        choices=AVAILABLE_STATUS,
        blank=True,
        default="a",
        help_text="Gift availability",
    )

    class Meta:
        ordering = ["id"]

    def __str__(self):
        """String for representing the GiftInstance object."""
        return f"{self.gift.name} {self.event_date}"

    def get_absolute_url(self):
        """Returns the url to access a detail record for this gift instance."""
        return reverse("giftinstance-update", args=[str(self.id)])


class Brand(models.Model):
    """Model representing a brand."""

    name = models.CharField(max_length=100, unique=True)
    est = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def get_absolute_url(self):
        """Returns the url to access a particular brand instance."""
        return reverse("brand-detail", args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"


class Country(models.Model):
    """Model representing a Country"""

    name = models.CharField(
        max_length=200, help_text="Enter the country the gift was made in",
        unique=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
