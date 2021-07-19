from rest_framework import serializers

from catalog.models import Category, Country


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = ["name"]

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]
