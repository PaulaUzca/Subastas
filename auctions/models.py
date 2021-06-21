from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, PROTECT
from django.db.models.fields import CharField, DateField
from django.db.models.fields import related
from django.db.models.fields.related import ForeignKey, ManyToManyField


class Gremio(models.Model):
    name = models.CharField(max_length=64)
    picture = models.URLField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    gremio = models.ForeignKey(Gremio, on_delete=models.CASCADE, related_name="miembros", blank=True , null=True)
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"


class ListingManager(models.Manager):
    def create_listing(self, owner,title,description,photo,category,price):
        listing = self.create(owner=owner, title=title, description=description,photo=photo,category=category,price=price)
        listing.save()
        bid = Bid(bidder=owner,article=listing,amount=price)
        bid.save()
        return listing


class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=CASCADE, related_name="listings")
    title = models.CharField(max_length=150)
    description = models.CharField(max_length=500)
    photo = models.URLField(max_length=200, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=CASCADE, related_name="listing", null=True, blank=True)
    price = models.PositiveIntegerField(default=0)
    closed = models.BooleanField(default=False)
    winner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="wins", blank=True, null=True)
    date = models.DateField(_("Date"), auto_now_add=True)
    watchers= models.ManyToManyField(User, related_name="watchlist")
    objects = ListingManager()
    
    def __str__(self):
        return f"{self.title} by {self.owner} Closed?{self.closed} price {self.bids.first()}"
    

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", blank=True, null=True)
    comment = models.TextField()
    date = models.DateField(_("Date"), auto_now_add=True)
    listing = models.ForeignKey(Listing, on_delete=CASCADE, related_name="comments")

    def __str__(self):
        return f"{self.user}: {self.comment} ({self.date})"


class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE ,related_name="bids")
    article = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.PositiveIntegerField(default=0)
    date = models.DateField(_("Date"), auto_now_add=True)

    def __str__(self):
        return f"{self.amount} {self.bidder}"

