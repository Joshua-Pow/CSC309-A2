from django import forms
from .models import Calendar
import datetime


class CalendarForm(forms.ModelForm):
    # Explicitly define start_date and end_date as CharFields for form input
    start_date = forms.CharField(
        required=True,
        error_messages={
            "required": "This field is required",
            "invalid": "Enter a valid date (YYYY-MM-DD)",
        },
    )
    end_date = forms.CharField(
        required=True,
        error_messages={
            "required": "This field is required",
            "invalid": "Enter a valid date (YYYY-MM-DD)",
        },
    )

    class Meta:
        model = Calendar
        fields = ["name", "description", "start_date", "end_date"]
        error_messages = {
            "name": {"required": "This field is required"},
        }

    def clean_start_date(self):
        start_date_str = self.cleaned_data.get("start_date")
        try:
            parsed_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise forms.ValidationError("Enter a valid date in YYYY-MM-DD format.")
        return parsed_date

    def clean_end_date(self):
        end_date_str = self.cleaned_data.get("end_date")
        try:
            parsed_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
        except ValueError:
            raise forms.ValidationError("Enter a valid date in YYYY-MM-DD format.")
        return parsed_date
