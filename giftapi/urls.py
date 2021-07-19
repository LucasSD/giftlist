from django.urls import include, path
from giftapi import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"countries", views.CountryViewSet)


urlpatterns = [
    path("", include(router.urls)),
]