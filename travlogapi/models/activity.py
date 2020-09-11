from django.db import models
from django.urls import reverse
from .day_itinerary import Day_itinerary

class Activity(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    day_itinerary = models.ForeignKey(Day_itinerary, related_name='activities', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("activity")
        verbose_name_plural = ("activitys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("activity_detail", kwargs={"pk": self.pk})