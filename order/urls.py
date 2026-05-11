from .views import addToCart,CartView
from django.urls import path

urlpatterns = [
    path('cart/',CartView.as_view(),name='cart'),
    path('cart-count/',addToCart.as_view(),name='cart-count'),
    path('add-to-cart/<int:pk>',addToCart.as_view(),name='add-to-cart'),
]