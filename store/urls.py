from django.urls import path
from .views import HomeView, ProductDetailView, ExploreView, ping
urlpatterns= [
    path("",HomeView.as_view(), name="home"),
    path("explore/", ExploreView.as_view(), name="explore"),
    path("product/<str:pk>",ProductDetailView.as_view(), name="product_detail"),
    path("ping/",ping, name="ping"),
]