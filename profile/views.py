from django.http import JsonResponse, HttpResponse
from django.views.generic import View
from .forms import ProfileEditForm
from django.shortcuts import render, redirect
from django.contrib.auth import login


class ProfileView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        user = request.user
        data = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "first_name": user.first_name,
            "last_name": user.last_name,
        }
        return JsonResponse(data)


class ProfileEdit(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        user = request.user
        form = ProfileEditForm(instance=user)
        return render(request, "profile/edit_profile.html", {"form": form})

    def post(self, request, *args, **kwargs):
        user = request.user
        if not user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        form = ProfileEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            if form.cleaned_data["password1"]:
                user.set_password(
                    form.cleaned_data["password1"]
                )  # User gets logged out when changing password
                login(request, user)
            user.save()
            return redirect("profile:view")
        return render(request, "profile/edit_profile.html", {"form": form})
