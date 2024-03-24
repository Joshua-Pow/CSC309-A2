from django.db import models
from django.contrib.auth.models import User
from django.contrib import admin


class Calendar(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class CalendarAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Calendar, CalendarAdmin)
