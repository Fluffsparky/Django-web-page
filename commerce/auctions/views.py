from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
import datetime
from .models import User, Listing , Bids, Comments, Catagory

class Newlisting(forms.Form):
    name = forms.CharField( max_length=64, label = "Item Name")
    start_bid = forms.FloatField(label = "Starting bid")
    catagory = forms.ModelChoiceField(queryset=Catagory.objects.all(),required=False)
    image = forms.URLField(required=False)
    discription = forms.CharField(widget=forms.Textarea,required=False)
    
class BidForm(forms.Form):
    bid = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': 0,
            }
        )
    )
class NewCommentForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Enter your comment here...',
        'rows': 3,
        'cols': 40
    }))


def index(request):
    return render(request, "auctions/index.html",{
        "listings": Listing.objects.all()
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
    
def newlisting(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = Newlisting(request.POST)
            if form.is_valid():
                table = Listing()
                table.name = form.cleaned_data["name"]
                table.start_bid = form.cleaned_data["start_bid"]
                table.catagory = form.cleaned_data["catagory"]
                table.image = form.cleaned_data["image"]
                table.description = form.cleaned_data["discription"]
                table.owner = request.user
                table.created = datetime.datetime.now()
                table.save()
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "auctions/addlisting.html", {
                        "user": request.user,
                        "form": form
                    })
        form = Newlisting()
        return render(request, "auctions/addlisting.html", {
                    "user": request.user,
                    "form": form
                })
    else:
        return HttpResponseRedirect("login")
    
    
def listing(request, item):
    listing = Listing.objects.filter(id=item).first()
    bids = Bids.objects.filter(listing = item).all()
    watchlist = listing.watchlist.all()
    comments = Comments.objects.filter(item = item).all()
    checked = False
    top_bidder = False
    winner = False
    if listing.winner.exists():
        winner = True
    if request.user in watchlist:
        checked = True
    top = 0.0
    if bids:    
        top = bids.order_by('-bid')[0]
        if top.user ==request.user:
            top_bidder = True 
    form = request.POST
    #save comment
    if request.method == "POST" and "message" in form:
        form = NewCommentForm(request.POST)
        if form.is_valid():
            comment = Comments()
            comment.username = request.user
            comment.message = form.cleaned_data["message"]
            comment.save()
            comment.item.set([listing])
        return HttpResponseRedirect(request.path_info)
    #save winner
    if request.method == "POST" and "End" in form:
        listing.winner.add(top.user)
        listing.save()
        return HttpResponseRedirect(request.path_info)
    #save watchlist
    if request.method == "POST" and "watchlist" in form:
        if not checked:
            listing.watchlist.add(request.user)
        else:
            listing.watchlist.remove(request.user)
        listing.save()
        return HttpResponseRedirect(request.path_info)
    #save bid
    elif request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            bid_amount = form.cleaned_data['bid']
            if top == 0.0 or bid_amount > top.bid :
                bid = Bids(listing=listing, user=request.user, bid=bid_amount)
                bid.save()
                return HttpResponseRedirect(request.path_info)
            else:
                form.add_error('bid', f'Your bid should be higher than R {top.bid}.')            
    else:
        form = BidForm()
    #default return
    return render(request, "auctions/listing.html", {
            "user": request.user,
            "item": listing,
            "max": top,
            "bids_ammount": len(bids),
            "watched" : checked,
            "top_bidder" : top_bidder,
            'form': form,
            "winner": winner,
            "comments": comments,
            "commentform" : NewCommentForm()
    })
def watchlist(request):
    if request.user.is_authenticated:
        user = request.user
        watchlist = Listing.objects.filter(watchlist=user)
        return render(request, "auctions/index.html",{
            "listings": watchlist,
            "watchlist" : True,
        })
    return HttpResponseRedirect("login")

def catagory(request):
    catagories = [catagory.catagory for catagory in Catagory.objects.all()]
    return render(request, "auctions/catagory.html",{
        "catagories" : catagories
    })

def filters(request, item):
    filtered = Listing.objects.filter(catagory=item)
    return render(request, "auctions/index.html",{
        "listings": filtered,
        "filter" : True,
        "catagory" : item
    })