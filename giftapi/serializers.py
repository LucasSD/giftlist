from rest_framework import serializers

from catalog.models import Brand, Category, Country, Gift


class CountrySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Country
        fields = ["name"]

class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = ["name"]

class BrandSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Brand
        fields = ["name", "est"]

class GiftSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Gift
        fields = ["name", "description", "ref"]

