from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import json

from .models import User, Post, Follower, post_max_length


def index(request):
    posts_list = Post.objects.all().order_by("-created_on")
    
    paginator = Paginator(posts_list, 10)
    
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "posts": posts,
        "post_max_length": post_max_length,
        "current_page": page_number,
        "page_range": range(posts.paginator.num_pages),
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
    
@csrf_exempt
def profile(request, user_id):
    user_profile = User.objects.get(id=user_id)
    
    followed, _ = Follower.objects.get_or_create(user=user_profile)
    is_following = request.user in followed.followers.all()
    
    if is_following:
        v_unfollow = "block"
        v_follow = "none"
    else:
        v_unfollow = "none"
        v_follow = "block"
    
    numbers_followed = followed.followers.count()
    number_follows = user_profile.following.count()
    
    posts = Post.objects.filter(user=user_profile).order_by("-created_on")
    
    if request.method == "PUT":
        if request.user == user_profile:
            return JsonResponse({"message": "You can't follow yourself"}, status=400)
        
        if request.user not in followed.followers.all():
            followed.followers.add(request.user)
            followed.save()
            
            return JsonResponse({"followed": True, "user_id": user_profile.id, "follower": request.user.id}, status=200)
        
        followed.followers.remove(request.user)
        followed.save()
        
        return JsonResponse({"followed": False, "user_id": user_profile.id, "follower": request.user.id}, status=200,)
    
    return render(request, "network/profile.html", {
        "user_profile": user_profile,
        "v_unfollow": v_unfollow,
        "v_follow": v_follow,
        "numbers_followed": numbers_followed,
        "number_follows": number_follows,
        "posts": posts,
        },
    )

@login_required
def follow(request):
    user = User.objects.get(id=request.user.id)
    follows = user.following.all()
    follows_user = [follow.user for follow in follows]
    
    posts_list = Post.objects.filter(user__in=follows_user).order_by("-created_on")
    
    paginator = Paginator(posts_list, 10)
    
    page_number = request.GET.get("page", 1)
    posts = paginator.get_page(page_number)
    
    return render(request, "network/follow.html", {
        "posts": posts,
        "current_page": page_number,
        "page_range": range(posts.paginator.num_pages),
        },
    )
    
@login_required
@csrf_exempt
def like(request, post_id):
    #if request.mehtod == "PUT":
    post = Post.objects.get(id=post_id)
    print(post)
   
    if request.user not in post.likes.all():
        post.likes.add(request.user)
        post.save()
    
        return JsonResponse({"like": True, "post_id": post_id}, status=200)
    
    post.likes.remove(request.user)
    post.save()
    
    return JsonResponse({"like": False, "post_id": post_id}, status=200,)


@login_required
def edit(request, post_id):
    pass