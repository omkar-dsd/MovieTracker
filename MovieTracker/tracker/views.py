from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from MovieTracker import settings
from django.contrib.auth.decorators import login_required
from django import forms
from tracker.models import UserWatched
import requests
import json
from django.core.urlresolvers import reverse



API_KEY = os.environ.get('TMDB_API_KEY')

# This view redirects to login
def gotoLogin(request):
    return HttpResponseRedirect(reverse('login'))

# View for login 
def Login(request):

	# This variable maintains the next state
    next = request.GET.get('next', '/unwatched/')
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                return HttpResponse("Inactive user.")
        else:
            return HttpResponseRedirect(settings.LOGIN_URL)

    return render(request, "tracker/login.html", {'redirect_to': next})

# View for Logging out the user
def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


# login is required for the following function Watched
@login_required
def Watched(request):

    watchedMovieIds = UserWatched.objects.values_list('movie_id', flat=True).filter(username=request.user)
    if(not watchedMovieIds):
        movies_list = None
    else:
        movies_list = getWatchedMovies(set(watchedMovieIds))

    return render(request, "tracker/watched.html", {'current_user':request.user,
                                                    'movies_list' : movies_list})

# View to add movies to watched list
@login_required
def AddToWatched(request, movieid):

    b = UserWatched(username=request.user, movie_id=movieid, movie_rating=10)
    b.save()

    return HttpResponseRedirect(reverse('unwatched'))

@login_required
def Unwatched(request,pageNumber=1):

    movies_list = getTopRated(request,pageNumber)

    return render(request, "tracker/unwatched.html", {'current_user':request.user,
                                                      'movies_list' : movies_list})

@login_required
def Movie(request):

    return render(request, "tracker/unwatched.html", {'current_user':request.user})


def Signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            # return redirect('tracker/home')
            return render(request, "tracker/watched.html", {})
    else:

        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})


def getTopRated(request,pageNumber):

    watchedMovieIds = UserWatched.objects.values_list('movie_id', flat=True).filter(username=request.user)

    topRatedList = []

    while(len(topRatedList)<100):
        r = requests.get("https://api.themoviedb.org/3/movie/top_rated?api_key=" + API_KEY +"&language=en-US&page="+str(pageNumber))
        movies = json.loads(r.text)

        if pageNumber>movies['total_pages']:
            return topRatedList
        else:
            for i in range(len(movies['results'])):
                if(movies['results'][i]['id'] in watchedMovieIds):
                    continue
                else:
                    movies['results'][i]['poster_path'] = "https://image.tmdb.org/t/p/w150" + movies['results'][i]['poster_path']
                    topRatedList.append(movies['results'][i])

        pageNumber+=1

    return topRatedList


def getWatchedMovies(idList):

    results = []

    for id in idList:
        url = "https://api.themoviedb.org/3/movie/" + str(id) + "?api_key=" + API_KEY +"&language=en-US"
        r = requests.get(url)
        movie = json.loads(r.text)
        movie['poster_path'] = "https://image.tmdb.org/t/p/w150" + movie['poster_path']
        results.append(movie)

    return results
