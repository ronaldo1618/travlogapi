from django.db import models
from django.urls import reverse
from .day_itinerary import Day_itinerary

class Food(models.Model):

    name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    notes = models.CharField(max_length=50)
    datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    cost = models.FloatField(null=True, blank=True)
    day_itinerary = models.ForeignKey(Day_itinerary, related_name='food', on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("food")
        verbose_name_plural = ("foods")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("food_detail", kwargs={"pk": self.pk})
