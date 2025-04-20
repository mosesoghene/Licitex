from rest_framework import serializers
from .models import Bid, AuctionItem
from django.utils import timezone


class BidSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bid
        fields = ('id', 'item', 'user', 'amount', 'timestamp')
        read_only_fields = ('id', 'user', 'timestamp')

    def validate_item(self, value):
        """
        Validate that the auction item exists and is active
        """
        if not value:
            raise serializers.ValidationError("Auction item is required")

        if value.auction_start > timezone.now() or value.auction_end < timezone.now():
            raise serializers.ValidationError("Auction is not active")
        return value

    def validate_amount(self, value):
        """
        Validate that the bid amount is greater than current bid
        """
        item = self.initial_data.get('item')
        if not item:
            return value

        try:
            auction_item = AuctionItem.objects.get(id=item)
            current_price = auction_item.current_bid or auction_item.starting_bid
            if value <= current_price:
                raise serializers.ValidationError(
                    f"Bid must be higher than current price of {current_price}"
                )
        except AuctionItem.DoesNotExist:
            raise serializers.ValidationError("Invalid auction item")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

