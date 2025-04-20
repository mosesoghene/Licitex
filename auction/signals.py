from django.db.models.signals import post_save
from django.db.models import F, Value, Case, When
from django.dispatch import receiver
from drf_yasg.openapi import logger

from .models import Bid, AuctionItem
from django.db import transaction

@receiver(post_save, sender=Bid)
def update_current_bid(sender, instance, created, **kwargs):
    if created:
        with transaction.atomic():
            updated_rows = AuctionItem.objects.filter(pk=instance.item.pk).update(
                current_bid=instance.amount,
                winner=instance.user,
            )
            if updated_rows != 1:
                raise ValueError(f"Failed to update current_bid for AuctionItem {instance.item.pk}")