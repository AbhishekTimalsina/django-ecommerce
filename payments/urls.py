from django.urls import path
from .views import PaymentView,ConfirmOrderView,OrderSuccessView

urlpatterns = [
    path('', PaymentView.as_view(), name="payment"),
    path('confirm/', ConfirmOrderView.as_view(), name="confirm_order"),
    path('<int:order_id>/success/', OrderSuccessView.as_view(), name="order_success")
]