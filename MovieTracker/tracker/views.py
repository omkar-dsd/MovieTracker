from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from MovieTracker import settings
from django.contrib.auth.decorators import login_required
from django import forms



# Keys:
#
# API Key (v3 auth)
# ca59847d10d1b5321571a0a279c95e61
# API Read Access Token (v4 auth)
# eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjYTU5ODQ3ZDEwZDFiNTMyMTU3MWEwYTI3OWM5NWU2MSIsInN1YiI6IjU5YzYzN2E2OTI1MTQxNWI2ZTAzZDc4NSIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.5pcWArPylqn1BxS5Lgsdn90li5_YfXD34OPhYG76-uY
# example request
# https://api.themoviedb.org/3/movie/550?api_key=ca59847d10d1b5321571a0a279c95e61

# Example Image url
# https://image.tmdb.org/t/p/w150/nl79FQ8xWZkhL3rDr1v2RFFR6J0.jpg

#Get movie detail
# https://api.themoviedb.org/3/movie/278?api_key=ca59847d10d1b5321571a0a279c95e61&language=en-US
class ColorForm(forms.Form):
    fav_color = forms.CharField(label='Fav Color', max_length=100)


def Login(request):
    next = request.GET.get('next', '/home/')
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

def Logout(request):
    logout(request)
    return HttpResponseRedirect(settings.LOGIN_URL)


# login is required for the following function Home
@login_required
def Home(request):
    if request.method == 'POST':

        form = ColorForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            request.session["fav_color"] = request.POST['fav_color']

            # return HttpResponseRedirect('/home/')
    else:
        form = ColorForm()

    if(not "fav_color" in request.session.keys()):
        # print "relksal;dfkm"
        request.session["fav_color"] = "Empty"

    return render(request, "tracker/home.html", {'fav_color':request.user,
                                                 'form':form})

def Blog(request):
    return render(request, "tracker/blog.html", {})


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
            return render(request, "tracker/home.html", {})
    else:

        form = UserCreationForm()
    return render(request, 'tracker/signup.html', {'form': form})