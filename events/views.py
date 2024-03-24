from django.views.generic.edit import FormView
from django.http import HttpResponse, Http404, HttpResponseForbidden
from .forms import EventForm
from .models import Calendar, Event
from django.views.generic import View, ListView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic.edit import UpdateView


class AddEventView(FormView):
    template_name = "events/add_event.html"
    form_class = EventForm
    success_url = "/calendars/event/{id}/details/"

    def dispatch(self, request, *args, **kwargs):
        self.calendar = None

        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)

        try:
            self.calendar = Calendar.objects.get(id=self.kwargs["calendar_id"])
            if self.calendar.owner != request.user:
                return HttpResponse("Forbidden", status=403)
        except Calendar.DoesNotExist:
            raise Http404("Calendar not found")
        return super(AddEventView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        event = form.save(commit=False)
        event.calendar = self.calendar
        event.owner = self.request.user
        event.save()
        self.success_url = self.get_success_url().format(id=event.id)
        return super(AddEventView, self).form_valid(form)


class EventEditView(UpdateView):
    model = Event
    form_class = EventForm
    template_name = "events/edit_event.html"
    context_object_name = "event"

    def get_success_url(self):
        return reverse_lazy("events:details", kwargs={"event_id": self.object.id})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponse("Unauthorized", status=401)
        event = self.get_object()
        if event.owner != request.user:
            return HttpResponseForbidden("Forbidden")
        return super().dispatch(request, *args, **kwargs)


class EventDetailsView(View):
    def get(self, request, *args, **kwargs):
        event = get_object_or_404(Event, id=self.kwargs["event_id"])
        data = {
            "id": event.id,  # type: ignore
            "name": event.name if request.user.is_authenticated else "",
            "description": event.description if request.user.is_authenticated else "",
            "date": event.date,
            "start_time": event.start_time,
            "duration": event.duration,
            "last_modified": event.last_modified,
        }
        return JsonResponse(data)


class AllEventsView(ListView):
    model = Event
    template_name = "events/list.html"
    context_object_name = "events"

    def get_queryset(self):
        calendar = get_object_or_404(Calendar, id=self.kwargs["calendar_id"])
        return Event.objects.filter(calendar=calendar).order_by("date", "start_time")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if not self.request.user.is_authenticated:
            for event in context["events"]:
                event.name = ""
        return context
