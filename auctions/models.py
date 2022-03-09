from django.contrib.auth.models import AbstractUser
from django.db import models
from asyncio.windows_events import NULL
from unittest.util import _MAX_LENGTH
from distutils.command.upload import upload

class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORY_CHOICES = [
        ('UN',''),
        ('CO','Computer'),
        ('EL','Electronics'),
        ('FA','Fashion'),
        ('GA','Garden'),
        ('HO','Home'),
        ('TO','Toy'),
        ('TR','Transport'),
    ]

    StatusType = models.TextChoices('StatusType', 'active sold')
    title      = models.CharField(max_length=64)
    descript   = models.CharField(max_length=250, blank=True, null=True)
    image      = models.ImageField(upload_to='image/', default="image/No_Photo.jpg")
    owner      = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    status     = models.CharField(max_length=6, choices=StatusType.choices, default="active") 
    created    = models.DateTimeField(auto_now_add=True)
    category   = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default="UN")
    price      = models.DecimalField(max_digits=7, decimal_places=2)
    watch      = models.ManyToManyField(User, related_name='watch_list')

    def __str__(self):
        return self.title

class Bid(models.Model):
    bid  = models.DecimalField(max_digits=7,decimal_places=2)
    list = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")


class List_comment(models.Model):
    comment = models.CharField(max_length=250, default='')
    user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comment")
    list    = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="list_comment")
