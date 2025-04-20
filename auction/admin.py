from django.contrib import admin

from auction.models import Bid, AuctionItem, Category


# Register your models here.
@admin.register(AuctionItem)
class AuctionItemAdmin(admin.ModelAdmin):
    list_display = ('item_name', 'starting_bid', 'current_bid', 'auction_start', 'auction_end', 'category', 'winner')
    list_filter = ('auction_start', 'auction_end', 'category')
    search_fields = ('item_name',)
    ordering = ('auction_start',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)

@admin.register(Bid)
class BidAdmin(admin.ModelAdmin):
    list_display = ('item', 'user', 'amount', 'timestamp')
    list_filter = ('timestamp', 'item')
    search_fields = ('item__item_name', 'user__username')
    ordering = ('-timestamp',)