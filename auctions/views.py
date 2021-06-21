from django import http
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.template.response import SimpleTemplateResponse, TemplateResponse
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.core import serializers

import datetime

from .forms import NewListingForm
from .models import Category, Comment, User, Gremio, Listing, Bid


def index(request):
    if request.user.is_authenticated:
        onwatchlist = request.user.watchlist.all()
    else:
        onwatchlist = None
    if request.method == "POST":
        key_toadd= request.POST.get('pk', None)
        if key_toadd is not None:
            listing = Listing.objects.get(id = key_toadd)
            addToWatchList(listing, request.user)
            return HttpResponse('all good')
        else:
            return HttpResponse('no succesful post requets')
    else:
        return render(request, "auctions/index.html", {
            'listings' : Listing.objects.all(),
            'userwatchlist': onwatchlist 
        })

def addToWatchList(listing, user):
    if user in listing.watchers.all():
        listing.watchers.remove(user)
    else:
        listing.watchers.add(user)

def must_addToWatchlist(listing, user):
    if user not in listing.watchers.all():
        listing.watchers.add(user)

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
        gremio = Gremio.objects.get(id = int(request.POST["gremio"]))
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
            user.gremio = gremio
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        gremios = Gremio.objects.all()
        return render(request, "auctions/register.html", {
            "gremios" : gremios
        })


def new_listing(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            category = form.cleaned_data['category']
            price = form.cleaned_data['price']
            photo = form.cleaned_data['photo']
            new_listing= Listing.objects.create_listing(owner= request.user, title = title, description= description, photo= photo, category= category, price= price)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request,"auctions/new-listing.html", {
                "form": form
            })
    else:
        if request.user.is_authenticated:
            return render(request, "auctions/new-listing.html", {
                'form' : NewListingForm(),
            })
        else:
            return render(request, "auctions/login.html", {
                'message': "Looks like you are not logged in yet!"
            })

def make_bid(request, pk):
    listing = Listing.objects.get(id = pk)
    rendered_comments = render_to_string("auctions/comments.html", {'comments': listing.comments.all()})
    rendered_bids = render_to_string("auctions/bids.html", {'bids': listing.bids.all()})
    current_bid = listing.bids.last()
    if request.method == "POST":
        listing.closed = True
        listing.winner= current_bid.bidder
        listing.save()
    return render(request, "auctions/make-bid.html", {
        'article' : listing,
        'comments': rendered_comments,
        'bids': rendered_bids,
        'currentbid': current_bid,
    })

def comment_manager(request):
    if request.method == "POST" and request.user.is_authenticated:
        listing = Listing.objects.get(id=request.POST['listing'])
        comment = Comment(
            user = request.user,
            comment= request.POST['comment'],
            date = datetime.datetime.now().date(),
            listing = listing)
        comment.save()
        context = {'comments': listing.comments.all()}
        rendered_comments = render_to_string("auctions/comments.html", context)
        return HttpResponse(rendered_comments)
    else:
        return HttpResponse("failed")

def bid_manager(request):
    if request.method == "POST" and request.user.is_authenticated:
        listing = Listing.objects.get(id=request.POST['listing'])
        bid = Bid(
            bidder=request.user,
            article=listing,
            amount= request.POST['bid'],
            date=datetime.datetime.now().date())
        bid.save()
        must_addToWatchlist(listing, request.user)
        context = {'bids': listing.bids.all()}
        rendered_bids = render_to_string("auctions/bids.html", context)
        return HttpResponse(rendered_bids)
    else:
        return HttpResponse("failed")

def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        'watchlist': request.user.watchlist.all()
    })

def category(request, category_name):
    category = Category.objects.get(name= category_name)
    listings_in_category = Listing.objects.filter(category=category)
    return render(request, 'auctions/index.html', {
        'listings': listings_in_category,
        'userwatchlist': request.user.watchlist.all(),
        'title': category.name
    })

def mylistings(request):
    user_listings = Listing.objects.filter(owner=request.user)
    return render(request, 'auctions/mylistings.html',{
        'mylistings': user_listings
    })