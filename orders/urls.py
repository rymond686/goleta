from django.urls import path

from .views import OrderHistoryView, order_create


urlpatterns = [
    path("", order_create, name="order-create"),
    path("orders/", OrderHistoryView.as_view(), name="order-history"),
]
