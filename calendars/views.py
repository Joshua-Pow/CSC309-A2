from django.views.generic.edit import FormView
from django.views.generic import DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CalendarForm
from .models import Calendar
from django.http import HttpResponse


class AddCalendarView(LoginRequiredMixin, FormView):
    template_name = "calendars/create.html"
    form_class = CalendarForm
    success_url = "/calendars/{id}/details/"

    def dispatch(self, request, *args, **kwargs):
        # Check if the user is authenticated
        if not request.user.is_authenticated:
            # Return a 401 Unauthorized response if the user is not authenticated
            return HttpResponse("Unauthorized", status=401)
        # Otherwise, proceed with the normal flow of the view
        return super(AddCalendarView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        calendar = form.save(commit=False)
        calendar.owner = self.request.user
        calendar.save()
        self.form = calendar
        return super().form_valid(form)

    def get_success_url(self):
        return f"/calendars/{self.form.id}/details/"


class CalendarDetailView(DetailView):
    model = Calendar
    template_name = "calendars/details.html"
    context_object_name = "calendar"
