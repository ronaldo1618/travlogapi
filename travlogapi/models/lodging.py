from django.db import models
from django.urls import reverse
from .day_itinerary import Day_itinerary

class Lodging(models.Model):

    day_itinerary = models.ForeignKey(Day_itinerary, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=100)
    website = models.CharField(max_length=100)
    check_in = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    check_out = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    notes = models.CharField(max_length=50)
    cost = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = ("lodging")
        verbose_name_plural = ("lodgings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lodging_detail", kwargs={"pk": self.pk})