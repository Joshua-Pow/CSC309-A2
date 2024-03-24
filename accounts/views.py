from django.views.generic import View
from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        form = RegisterForm()
        return render(request, "accounts/register.html", {"form": form})

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
        return render(request, "accounts/register.html", {"form": form})


class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "accounts/login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                return redirect("profile:view")  # Redirect to a success page.
            else:
                return render(
                    request,
                    "accounts/login.html",
                    {"form": form, "error_message": "Username or password is invalid"},
                )
        else:
            return render(
                request,
                "accounts/login.html",
                {"form": form, "error_message": "Username or password is invalid"},
            )

        return render(request, "accounts/login.html", {"form": form})


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect("login")
