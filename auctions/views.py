from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max  # new
from django.contrib.auth.decorators import login_required  # new

from .models import User, Listing, Bid, List_comment
from .forms import createListingForm, createBidForm, createCommentForm




def index(request):
    context = {
        "listings": Listing.objects.filter(status='active'),
        "listtype": 'Active Listings',
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    }
    return render(request, "auctions/index.html", context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def createListing(request):
    if request.method == "POST":
        list_form = createListingForm(request.POST, request.FILES)
        if list_form.is_valid():
            list_form.cleaned_data
            list_form.save()
            return render(request, "auctions/createListing.html", {
                "list_form": createListingForm(),
                "message": "Database opdated!",
                "w_antal": Listing.objects.filter(watch__id=1).values_list('id', flat=True).count(),
            })
        else:
            # If the form is invalid, re-render the page with existing information.
            return render(request, "auctions/createListing.html", {
                "list_form": list_form,
                "message": "Form is invalid",
                "w_antal": Listing.objects.filter(watch__id=1).values_list('id', flat=True).count(),
            })

    return render(request, "auctions/createListing.html", {
        "list_form": createListingForm(),
        "w_antal": Listing.objects.filter(watch__id=1).values_list('id', flat=True).count(),
    })

def listing(request, list_id):
    list     = Listing.objects.get(id=list_id)
    w_users = User.objects.filter(watch_list__id=list_id).values_list('id', flat=True)  
    bids_all = Bid.objects.filter(list=list_id).count()
    if bids_all:
        t = Bid.objects.filter(list=list_id)
        bid_user = t[bids_all - 1].user.id    
    else:
        bid_user = 0
        
    return render(request, "auctions/listing.html", {
        "list": list,
        "lComment": List_comment.objects.filter(list=list_id),
        "bids_all": bids_all,
        "bid_user": bid_user,
        "w_users": User.objects.filter(watch_list__id=list_id).values_list('id', flat=True),
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
        "bid_form": createBidForm(),
        "comment_form": createCommentForm(),
    })

def categoryList(request):
    return render(request, "auctions/category.html", {
        "catList": Listing.CATEGORY_CHOICES,
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    })        

@login_required
def addBid(request, list_id):
    if request.method == "POST":
        list     = Listing.objects.get(id=list_id)
        bid_form = createBidForm(request.POST)
        context = {
            "list": list,
            "bid_form": bid_form,
            "bids_all": Bid.objects.filter(list=list_id).count(),
            "w_users": User.objects.filter(watch_list__id=list_id).values_list('id', flat=True),
            "w_antal": Listing.objects.filter(watch__username=request.user).count(),
            "lComment": List_comment.objects.filter(list=list_id),
        }
        if bid_form.is_valid():
            bid = bid_form.cleaned_data['bid']
            price = list.price
            if float(bid) > float(price):
                bid_form.save()
                list.price = bid
                list.save()
                # Listing skal opdateres med nye bid
                return HttpResponseRedirect(reverse('listing', args=(list_id, )))
            else:
                message = {"message_bid" : "Bid not accepted. Too small"}
                context.update(message)
                return render(request, 'auctions/listing.html', context)

        else:
            # If the form is invalid, re-render the page with existing information.
            message =  {"message_bid": "Form is invalid"}
            context.update(message)
            return render(request, 'auctions/listing.html', context)

    #  Listing skal opdaters med nye bid value
    list     = Listing.objects.get(id=list_id)
    return render(request, "auctions/listing.html", {
        "list": list,
        "bid_form": createBidForm(),
    })

@login_required
def addComment(request, list_id):
    bids_all = Bid.objects.filter(list=list_id).count()
    if bids_all:
        t = Bid.objects.filter(list=list_id)
        bid_user = t[bids_all - 1].user.id    
    else:
        bid_user = 0
    context = {
        "list": Listing.objects.get(id=list_id),
        "lComment": List_comment.objects.filter(list=list_id),
        "bids_all": bids_all,
        "bid_user": bid_user,
        "bid_form": createBidForm(),
        "comment_form": createCommentForm(),
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    }

    if request.method == "POST":
        comment_form = createCommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
        else:
            # If the form is invalid, re-render the page with existing information.
            message = {"message_comment": "Form is invalid"}
            context.update(message)
            return render(request, 'auctions/listing.html', context)
    
    return render(request, "auctions/listing.html", context)

def watchlist(request, list_id):
    if request.method == "POST":
        funkt = request.POST['funktion']
        us    = request.POST['user']
        li    = request.POST['list']

        if funkt == 'add':
            Listing.objects.get(id=li).watch.add(User.objects.get(id=us))
        if funkt == 'remove':
            Listing.objects.get(id=li).watch.remove(User.objects.get(id=us))

    return HttpResponseRedirect(reverse('listing', args=(list_id, )))

def showWatchlist(request, user_id):
    listings = Listing.objects.filter(watch__id=user_id) 
    return render(request, "auctions/index.html", {
        "listings": listings,
        "listtype": 'Watch list',
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    })

def acceptBid(request, list_id):
    if request.method == "POST":
        list     = Listing.objects.get(id=list_id)
        list.status = 'sold'
        list.save()
    return render(request, "auctions/index.html", {
        "listings": Listing.objects.filter(status='active'),
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    })

def showCategorylist(request, category):
    listings = Listing.objects.filter(category=category, status='active')  
    if listings:
        aktuel_cat = listings[0].get_category_display()
    else:
        aktuel_cat = 'No '
    listtype = aktuel_cat + ' Listing'
    return render(request, "auctions/index.html", {
        "listings": listings,
        "listtype": listtype,
        "w_antal": Listing.objects.filter(watch__username=request.user).count(),
    })