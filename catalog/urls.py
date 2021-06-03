from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('gifts/', views.GiftListView.as_view(), name='gifts'),
    path('gift/<int:pk>', views.GiftDetailView.as_view(), name='gift-detail'),
    path('brands/', views.BrandListView.as_view(), name='brands'),
    path('brand/<int:pk>', views.BrandDetailView.as_view(), name='brand-detail'),
]