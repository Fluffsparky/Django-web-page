from django.contrib.auth.models import AbstractUser
from django.db import models
import datetime

class User(AbstractUser):
    id = models.AutoField(primary_key=True)
    pass

class Listing(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField( max_length=64)
    start_bid = models.FloatField()
    created = models.DateTimeField()
    catagory = models.CharField( max_length=64,blank=True,null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.URLField( max_length=500,blank=True,null=True)
    description = models.TextField(null=True, blank=True)
    watchlist = models.ManyToManyField(User ,blank=True, related_name="watched")
    winner = models.ManyToManyField(User ,blank=True, related_name="won")
    def __str__(self):
        return F"{self.name} ({self.start_bid})"

class Bids(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.FloatField(default=0)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    def __str__(self):
        return F"R{self.bid} for ({self.listing.name})"

class Comments(models.Model):
    id = models.AutoField(primary_key=True)
    item = models.ManyToManyField(Listing ,blank=True, related_name="item")
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default=None)
    created_date = models.DateTimeField(default=datetime.datetime.now())
    def __str__(self):
        return F"{self.username} ({self.message})"
    
class Catagory(models.Model):
    catagory = models.CharField(max_length=64,primary_key= True)
    def __str__(self):
        return self.catagory