from django.db import models
from django.urls import reverse

import uuid # Required for unique book instances

class Category(models.Model):
    """Model representing a gift category."""
    name = models.CharField(max_length=200, help_text='Enter a gift category (e.g. electronics or clothes)')

    def __str__(self):
        """String for representing the Model object."""
        return self.name

class Gift(models.Model):
    """Model representing a Gift (but not a gift instance which a user has requested)."""
    name = models.CharField(max_length=200)

    # Foreign Key used because gift should only have one brand, but a brand can make multiple gifts
    # Brand as a string rather than object because it hasn't been declared yet in the file
    brand = models.ForeignKey("catalog.brand", on_delete=models.RESTRICT, null=True)

    description = models.TextField(max_length=1000, help_text='Enter a brief description of the gift')
    ref = models.CharField(max_length=20, unique=True,
                             help_text="Enter a product code or similar as a reference")

    # ManyToManyField used because category can contain many gifts. Gifts can cover many categories.
    category = models.ManyToManyField(Category, help_text='Select a category for this gift')

    # Foreign Key used because gift should only have one made_in(country), but a country can make multiple gifts
    # Made_in as a string rather than object because it hasn't been declared yet in the file
    made_in = models.ForeignKey('Country', on_delete=models.RESTRICT, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    url = models.URLField()

    def __str__(self):
        """String for representing the Model object."""
        return self.name

    def get_absolute_url(self):
        """Returns the url to access a detail record for this gift."""
        return reverse('gift-detail', args=[str(self.id)])

class GiftInstance(models.Model):
    """Model representing a specific copy of a gift that appear on lists (i.e. that can be taken by a buyer)."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this specific gift requested by a single user')
    gift = models.ForeignKey(Gift, on_delete=models.RESTRICT, null=True)
    event_date = models.DateField(null=True, blank=True)

    AVAILABLE_STATUS = (
        ('a', 'Available'),
        ('t', 'Taken'),
    )

    status = models.CharField(
        max_length=1,
        choices=AVAILABLE_STATUS,
        blank=True,
        default='a',
        help_text='Gift availability',
    )

    class Meta:
        ordering = ['id']

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.id} ({self.gift.name})'

class Brand(models.Model):
    """Model representing a brand."""
    name = models.CharField(max_length=100)
    est = models.DateField(null=True, blank=True)
    gift = models.ForeignKey(Gift, on_delete=models.RESTRICT, null=True)
    
    class Meta:
        ordering = ['name']

    def get_absolute_url(self):
        """Returns the url to access a particular brand instance."""
        return reverse('brand-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return f"{self.name}"