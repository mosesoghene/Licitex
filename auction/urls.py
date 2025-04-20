from django.urls import path
from .views import BidCreateAPIView, ActiveAuctionItemListAPIView

urlpatterns = [
    path('bids/create/', BidCreateAPIView.as_view(), name='bid-create'),
    path('active/', ActiveAuctionItemListAPIView.as_view(), name='active-auctions-list'),
]