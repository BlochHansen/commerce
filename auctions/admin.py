from django.contrib import admin

from auctions.forms import watchForm
from .models import User, Listing, Bid, List_comment

# Register your models here.
admin.site.register(User)
admin.site.register(Listing)
admin.site.register(Bid)
admin.site.register(List_comment)

