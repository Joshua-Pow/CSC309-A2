from django.urls import path, include
from .views import AddCalendarView, CalendarDetailView


urlpatterns = [
    path("add/", AddCalendarView.as_view(), name="add_calendar"),
    path(
        "<int:pk>/details/",
        CalendarDetailView.as_view(),
        name="calendar_details",
    ),
    path(
        "<int:calendar_id>/events/", include("events.urls", namespace="calendar_events")
    ),  # TODO: event vs eventS, notice the s at the end
    path("event/", include("events.urls", namespace="individual_event")),
]
