from django.urls import path
from .views import BidCreateAPIView, ActiveAuctionItemListAPIView, AuctionItemCreateAPIView

urlpatterns = [
    path('place/bid/', BidCreateAPIView.as_view(), name='bid-create'),
    path('view/active/items/', ActiveAuctionItemListAPIView.as_view(), name='active-auctions-list'),
    path('create/auction/item/', AuctionItemCreateAPIView.as_view(), name='auction-item-create'),
]