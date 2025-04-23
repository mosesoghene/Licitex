from django.contrib.auth import get_user_model
from django.utils.text import slugify
from rest_framework import serializers
from .models import Bid, AuctionItem, Category
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
            auction_start = auction_item.auction_start
            auction_end = auction_item.auction_end
            current_time = timezone.now()

            if auction_start < current_time > auction_end:
                raise serializers.ValidationError("Bidding for auction item is not allowed at this time")

            if value <= current_price:
                raise serializers.ValidationError(f"Bid must be higher than current price of {current_price}")

        except AuctionItem.DoesNotExist:
            raise serializers.ValidationError("Invalid auction item")
        return value

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user.username
        return super().create(validated_data)

User = get_user_model()
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class AuctionItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    winner = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = AuctionItem
        fields = ('id', 'item_name', 'starting_bid', 'current_bid',
                  'auction_start', 'auction_end', 'category', 'winner', 'creator')
        read_only_fields = ('id', 'item_name', 'auction_start', 'auction_end', 'winner', 'current_bid')


class AuctionItemCreateSerializer(serializers.ModelSerializer):
    category = serializers.CharField(max_length=100)

    class Meta:
        model = AuctionItem
        fields = ('item_name', 'starting_bid', 'auction_start', 'auction_end', 'category')

    def validate_category(self, value):
        return value.strip().title()

    def validate(self, data):
        if data['auction_start'] >= data['auction_end']:
            raise serializers.ValidationError("Auction end must be after start time")

        if data['auction_start'] < timezone.now():
            raise serializers.ValidationError("Auction cannot start in the past")

        if data['starting_bid'] <= 0:
            raise serializers.ValidationError("Starting bid must be positive")

        return data

    def create(self, validated_data):
        category_name = validated_data.pop('category')

        category, created = Category.objects.get_or_create(
            name=category_name,
            defaults={'slug': slugify(category_name)}
        )

        return AuctionItem.objects.create(
            category=category,
            creator=self.context['request'].user,
            **validated_data
        )