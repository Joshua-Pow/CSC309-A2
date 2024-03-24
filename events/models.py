from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin
from calendars.models import Calendar


class Event(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes", default=30)
    calendar = models.ForeignKey(
        Calendar, on_delete=models.CASCADE, related_name="events"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    last_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class EventAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Event, EventAdmin)
