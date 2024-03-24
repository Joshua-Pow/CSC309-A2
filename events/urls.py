from django.urls import path
from .views import AddEventView, EventDetailsView, AllEventsView, EventEditView

app_name = "events"

urlpatterns = [
    path("all/", AllEventsView.as_view(), name="all"),
    path("add/", AddEventView.as_view(), name="add"),
    path("<int:pk>/edit/", EventEditView.as_view(), name="edit_event"),
    path("<int:event_id>/details/", EventDetailsView.as_view(), name="details"),
]
