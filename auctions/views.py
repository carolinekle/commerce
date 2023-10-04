from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Listing, Bid, Comment

from .models import User


def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html",{
        "listings":active_listings
    })


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
        
def create(request):
    if request.method == "POST":
   
        title = request.POST["title"]
        description = request.POST["description"]
        img = request.POST["img"]
        price = request.POST["price"]
        cat = request.POST["category"]
        new_cat = request.POST["newCat"]
        seller = request.user
        
        if new_cat is not None:
            cat=new_cat

        new_listing = Listing(
            title=title,
            description=description,
            image=img,
            category=cat,
            amount=float(price),
            seller=seller
            )
        new_listing.save()

        return HttpResponseRedirect(reverse(index))
    else:
        categories = Listing.objects.values_list('category', flat=True).distinct()   
        return render(request, "auctions/create.html", {
            "categories":categories
        })

def listing_page(request, listing_id):
    listing = Listing.objects.get(id=listing_id)
    return render(request, "auctions/listing.html",{
        "listing":listing
    })

def add_watcher(request, listing_id):

    watcher=request.user
    listing = Listing.objects.get(id=listing_id)

    if listing.watchlist.filter(watcher).exists():
        #"watchlist_message":"Remove from watchlist"
        #return render^ with dictionary
        listing.watchlist.add(watcher)
        listing.save()
        #else
            #add watcher with redirect and different message

    return HttpResponseRedirect(reverse(listing, args=(listing_id, )))

