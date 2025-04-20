from django.urls import path
from .views import BidCreateAPIView

urlpatterns = [
    path('bids/create/', BidCreateAPIView.as_view(), name='bid-create'),
]