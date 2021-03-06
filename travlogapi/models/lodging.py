from django.db import models
from django.urls import reverse
from .day_itinerary import Day_itinerary

class Lodging(models.Model):

    day_itinerary = models.ForeignKey(Day_itinerary, related_name='lodging', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100, null=True)
    phone_number = models.CharField(max_length=100, null=True)
    website = models.CharField(max_length=100, null=True)
    check_in = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    notes = models.CharField(max_length=50, null=True)
    cost = models.FloatField(null=True, blank=True)

    class Meta:
        verbose_name = ("lodging")
        verbose_name_plural = ("lodgings")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("lodging_detail", kwargs={"pk": self.pk})