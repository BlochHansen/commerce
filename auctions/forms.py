from secrets import choice
from socket import fromshare
from tkinter import Image
from turtle import textinput
from django import forms
from .models import Listing, Bid, List_comment
from django.forms import TextInput, FileInput, HiddenInput, Select

class createListingForm(forms.ModelForm):
    """ Form for the image model"""
    class Meta:
        model = Listing
        fields = ('title','descript','price','image','owner','category')

        widgets = {
            'title': TextInput(attrs={
                'class': "form-control",
                'label': "ANDERS",
                # 'placeholder': 'Title',
            }),
            'descript': TextInput(attrs={
                'class': "form-control",
                # 'placeholder': 'Description'
            }),
            'price': TextInput(attrs={
                'class': "form-control",
                # 'placeholder': 'Price'
            }),
            'image': FileInput(attrs={
                'class': "form-control",
            }),
            'owner': HiddenInput(attrs={
                'class': "form-control",
            }),
            'category': Select(attrs={
                'class': "form-control",
            })
        }

class createBidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('bid', 'list', 'user')


class createCommentForm(forms.ModelForm):
    class Meta:
        model = List_comment
        fields = ('comment', 'user', 'list')

class watchForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ('watch',)

