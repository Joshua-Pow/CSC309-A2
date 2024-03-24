from django import forms
from .models import Event
import datetime


class EventForm(forms.ModelForm):
    # Explicitly define start_date and end_date as CharFields for form input
    date = forms.CharField(
        required=True,
        error_messages={
            "required": "This field is required",
            "invalid": "Enter a valid date (YYYY-MM-DD)",
        },
    )

    start_time = forms.TimeField(widget=forms.TimeInput(format="%H:%M"))

    class Meta:
        model = Event
        fields = ["name", "description", "date", "start_time", "duration"]
        error_messages = {
            "name": {"required": "This field is required"},
            "date": {
                "required": "This field is required",
                "invalid": "Enter a valid date (YYYY-MM-DD)",
            },
            "start_time": {
                "required": "This field is required",
                "invalid": "Enter a valid time (hh:mm)",
            },
            "duration": {"required": "This field is required"},
        }

    def clean_date(self):
        date_str = self.cleaned_data.get("date")
        try:
            parsed_date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            raise forms.ValidationError("Enter a valid date in YYYY-MM-DD format.")
        return parsed_date

    def clean_start_time(self):
        time_input = self.cleaned_data.get("start_time")
        # Convert time to string in HH:MM format
        time_str = time_input.strftime("%H:%M")
        # Re-parse to ensure it's strictly HH:MM with no seconds
        try:
            valid_time = datetime.datetime.strptime(time_str, "%H:%M").time()
        except ValueError:
            raise forms.ValidationError("Enter a valid time in HH:MM format.")
        return valid_time
