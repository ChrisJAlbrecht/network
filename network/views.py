from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, Post, Follower, post_max_length


def index(request):
    posts = Post.objects.all().order_by("-created_on")
    
    # paginator
    
    return render(request, "network/index.html", {
        "posts": posts,
        "post_max_length": post_max_length,
        },
    )


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


def post(request, post_id=None):
    if request.method == "POST":
        user = User.objects.get(id=request.user.id)
        post = Post.objects.create(
            user=user, post=request.POST["post-message"]
        )
        #post.likes.add(user)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
    
def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    
    followed, _ = Follower.objects.get_or_create(user=user_profile)
    is_following = request.user in followed.followers.all()
    
    numbers_followed = followed.followers.count()
    number_follows = user_profile.following.count()
    
    posts = Post.objects.filter(user=user_profile).order_by("-created_on")
    
    # paginator
    
    return render(request, "network/profile.html", {
        "user": user_profile,
        "following": is_following,
        "numbers_followed": numbers_followed,
        "number_follows": number_follows,
        "posts": posts,
        },
    )