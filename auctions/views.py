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
    watchlist_message = request.GET.get('w_message', '')
    listing = Listing.objects.get(id=listing_id)
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html",{
        "listing":listing,
        "watchlist_message": watchlist_message,
        "comments":comments
    })

def add_watcher(request, listing_id):
    if request.method == "POST":
        watcher=request.user
        listing = Listing.objects.get(pk=listing_id)

        if watcher in listing.watchlist.all():
            listing.watchlist.remove(watcher)
            listing.save()
            return HttpResponseRedirect(reverse("listing_page",  args=[listing_id]))

        else:
            listing.watchlist.add(watcher)
            listing.save()
            return HttpResponseRedirect(reverse("listing_page", args=[listing_id]) + "?w_message=Remove%20from%20watchlist")
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))
    
def watchlist_page(request):
    user=request.user
    watched_listings=user.ListingWatchlist.all()
    return render(request, "auctions/watching.html", {
        "listings":watched_listings
    })
    
def categories_page(request):
    if request.method == "POST":
        selected_category = request.POST["category"]
        active_listings_by_cat=Listing.objects.filter(active=True, category=selected_category)
        return render(request, "auctions/index.html", {
            "listings":active_listings_by_cat
        })
    else:
        categories = Listing.objects.values_list('category', flat=True).distinct()   
        return render(request, "auctions/cat.html", {
            "categories":categories
        })

def add_comment(request, listing_id):
    this_commenter = request.user
    text = request.POST["new_comment"]
    this_listing= Listing.objects.get(id=listing_id)

    new_comment = Comment(
        comment_text=text,
        commenter=this_commenter,
        listing=this_listing
    )
    new_comment.save()
    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))

def place_bid():
    return
"""
    if request.method == "POST":
        this_bidder = request.user
        new_bid_price = request.POST["new_bid"]

        this_listing = Listing.objects.get(id=listing_id)
        
        current_bid = Bid.objects.filter(bid_listing=this_listing).order_by('-bid_amount').first()

        if current_bid is None or new_bid_price > current_bid.bid_amount:
            new_bid = Bid(
                bidder=this_bidder,
                bid_amount=new_bid_price,
                bid_listing=this_listing  
            )
            new_bid.save()
            return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))
    else:
        return HttpResponseRedirect(reverse("listing_page", args=[listing_id])) """