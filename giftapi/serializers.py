from rest_framework import serializers

from catalog.models import Country


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = ["name"]
