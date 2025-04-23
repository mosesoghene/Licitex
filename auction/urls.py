from django.urls import path
from .views import BidCreateAPIView, ActiveAuctionItemListAPIView, home_view, AuctionItemCreateAPIView

urlpatterns = [
    path('/', home_view, name='home'),
    path('auction/bids/create/', BidCreateAPIView.as_view(), name='bid-create'),
    path('auction/active/', ActiveAuctionItemListAPIView.as_view(), name='active-auctions-list'),
    path('auction/item/create/', AuctionItemCreateAPIView.as_view(), name='auction-item-create'),
]