from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from MovieTracker import settings
from django.contrib.auth.decorators import login_required

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
    return render(request, "tracker/home.html", {})

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