import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import timezone
from rest_framework import generics, status, permissions
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Bid, AuctionItem
from .serializers import BidSerializer, AuctionItemSerializer, AuctionItemCreateSerializer
from rest_framework.response import Response

class BidCreateAPIView(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = BidSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class ActiveAuctionItemListAPIView(generics.ListAPIView):
    serializer_class = AuctionItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Return a queryset of active auction items (where current time is between auction_start and auction_end)
        """
        now = timezone.now()
        return AuctionItem.objects.filter(
            auction_start__lte=now,
            auction_end__gte=now
        ).order_by('auction_end')


class AuctionItemCreateAPIView(generics.CreateAPIView):
    serializer_class = AuctionItemCreateSerializer
    permission_classes = [IsAuthenticated]



class EndedAuctionItemListAPIView(generics.ListAPIView):
    serializer_class = AuctionItemSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        """
        Return a queryset of ended auction items (where current time is greater that auction_end)
        """
        now = timezone.now()
        return AuctionItem.objects.filter(
            auction_end__lte=now
        ).order_by('-auction_end')


def home_view(request):
    return  redirect("/swagger")