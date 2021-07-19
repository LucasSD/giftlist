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
