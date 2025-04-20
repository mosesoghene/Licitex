from django.db.models.signals import post_save
from django.db.models import F, Value, Case, When
from django.dispatch import receiver
from .models import Bid, AuctionItem
from django.db import transaction

@receiver(post_save, sender=Bid)
def update_current_bid(sender, instance, created, **kwargs):
    if created:
        try:
            with (transaction.atomic()):
                AuctionItem.objects \
                .filter(pk=instance.item.pk,)\
                .update(
                    current_bid=Case(
                        When(
                            current_bid__lt=instance.amount,
                            then=Value(instance.amount)
                        ),
                        default=F('current_bid')
                    )
                )
        except Exception as e:
            logger.error(f"Bid update failed: {str(e)}")