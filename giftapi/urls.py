from django.urls import include, path
from giftapi import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r"countries", views.CountryViewSet)
router.register(r"categories", views.CategoryViewSet)
router.register(r"brands", views.BrandViewSet)
router.register(r"gifts", views.GiftViewSet)


urlpatterns = [
    path("", include(router.urls)),
]