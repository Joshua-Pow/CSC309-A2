from django.urls import path
from .views import ProfileEdit, ProfileView

app_name = "profile"

urlpatterns = [
    path("view/", ProfileView.as_view(), name="view"),
    path("edit/", ProfileEdit.as_view(), name="edit"),
]
