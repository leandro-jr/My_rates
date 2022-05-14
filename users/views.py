from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import LoginForm


# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    return render(request, "users/user.html")


def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "users/login.html", {"message": "Invalid Credentials.",
                                                            "login_form": LoginForm()
                                                            })
    else:
        return render(request, "users/login.html", {"login_form": LoginForm()})


def logout_view(request):
    logout(request)
    return render(request, "users/login.html", {"message": "Logged out.", "login_form": LoginForm()})
