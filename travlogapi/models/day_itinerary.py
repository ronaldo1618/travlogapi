from django.db import models
from django.urls import reverse
from .trip import Trip

class Day_itinerary(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("day_itinerary")
        verbose_name_plural = ("day_itinerarys")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("day_itinerary_detail", kwargs={"pk": self.pk})