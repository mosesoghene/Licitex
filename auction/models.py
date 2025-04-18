from django.db import models

# Create your models here.
class AuctionItem(models.Model):
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    winner = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)

    @property
    def auction_date(self):
        return self.auction_start.date()

    class Meta:
        indexes = [
            models.Index(fields=['auction_start', 'auction_end']),
        ]
        ordering = ['auction_start']
        verbose_name = 'Auction Item'
        verbose_name_plural = 'Auction Items'


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
