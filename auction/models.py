from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.
class AuctionItem(models.Model):
    item_name = models.CharField(max_length=100)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    auction_start = models.DateTimeField()
    auction_end = models.DateTimeField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    winner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.item_name} | {self.category.name}"

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

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Bid(models.Model):
    item = models.ForeignKey(
        AuctionItem,
        on_delete=models.CASCADE,
        related_name='bids'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_bids'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        """
        Ensures bid amount exceeds current price and starting bid
        """
        super().clean()

        if not self.id:
            current_price = self.item.current_bid or self.item.starting_bid

            if self.amount <= current_price:
                raise ValidationError(f"Bid must be higher than {current_price:.2f}")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp', 'item', '-amount']),
        ]