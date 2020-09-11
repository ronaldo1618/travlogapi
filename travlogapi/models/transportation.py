from django.db import models
from django.urls import reverse
from .day_itinerary import Day_itinerary

class Transportation(models.Model):

    name = models.CharField(max_length=50)
    dep_datetime = models.DateTimeField(auto_now_add=True)
    dep_info = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    arr_info = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    cost = models.FloatField(null=True, blank=True)
    day_itinerary = models.ForeignKey(Day_itinerary, related_name='transportation', on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = ("transportation")
        verbose_name_plural = ("transportations")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("transportation_detail", kwargs={"pk": self.pk})