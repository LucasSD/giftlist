from rest_framework import mixins
from rest_framework import viewsets

from catalog import models
from . import serializers

class CountryViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
    New countries are created from the country list. 
    """
    queryset = models.Country.objects.all()
    serializer_class = serializers.CountrySerializer

class CategoryViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
    New categories are created from the category list. 
    """
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer

class BrandViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
    New brands are created from the brand list. 
    """
    queryset = models.Brand.objects.all()
    serializer_class = serializers.BrandSerializer

class GiftViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                viewsets.GenericViewSet):
    """
    New gifts are created from the gift list. 
    """
    queryset = models.Gift.objects.all()
    serializer_class = serializers.GiftSerializer
