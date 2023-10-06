from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
#    comments = models.ManyToManyField(Comment, blank=True)
#    listings = models.ManyToManyField(Listing, blank=True)
#    bids = models.ManyToManyField(bids, blank=True)

class Listing(models.Model):
    amount = models.FloatField()
    title = models.CharField(max_length=64)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=300)
    image = models.CharField(max_length=2000)
    category = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="ListingWatchlist")

    def __str__(self):
        return f"{self.id} ({self.title})"

class Bid(models.Model):
    amount = models.FloatField()
    bidder = models.ForeignKey(User, on_delete=models.CASCADE)

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="User")
    comment_text = models.CharField(max_length=240)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=True, null=True, related_name="listing")
    
    def __str__(self):
        return f"{self.commenter} comment on ({self.listing})"
