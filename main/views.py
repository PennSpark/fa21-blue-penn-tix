from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from main.models import Tweet
from datetime import datetime

def main_view(request):
    if not request.user.is_authenticated:
        return render(request, 'splash.html')

    if request.method == 'POST' and request.POST['body'] != "":
        tweet = Tweet.objects.create(
            body = request.POST['body'],
            author = request.user,
            created_at = datetime.now()
        )
        tweet.save()

    tweets = Tweet.objects.all().order_by('-created_at')
    return render(request, 'main.html', {'tweets': tweets})

def delete_view(request):
    tweet = Tweet.objects.get(id=request.GET['id'])
    if tweet.author == request.user:
        tweet.delete()
    return redirect('/')

def like_tweet(request):
    tweet = Tweet.objects.get(id=request.GET['id'])

    if len(tweet.likes.filter(username=request.user.username)) == 0:
        tweet.likes.add(request.user)
    else:
        tweet.likes.remove(request.user)

    tweet.save()
    return redirect('/')

def splash_view(request):
    return render(request, 'splash.html' )

def login_view(request):
    username, password = request.POST['username'], request.POST['password']
    user = authenticate(username=username, password=password)

    if user is not None:
        login(request, user)
        return redirect('/')
    else:
        return redirect('/splash?error=LoginError')

def signup_view(request):
    user = User.objects.create_user(
        username=request.POST['username'],
        password=request.POST['password'],
        email=request.POST['email'],
    )
    login(request, user)
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/splash')