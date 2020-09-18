from django.db import models
from django.urls import reverse
from .traveler import Traveler
from datetime import date

class Trip(models.Model):

    creator = models.ForeignKey(Traveler, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=300, null=True)
    overlay_image = models.CharField(max_length=300, null=True)
    start_date = models.DateField(auto_now_add=False, null=True, blank=True)
    end_date = models.DateField(auto_now_add=False, null=True, blank=True)
    is_public = models.BooleanField()
    homepage_trip = models.BooleanField()
    trip_length = models.IntegerField()
    date_created = models.DateField(auto_now_add=True, null=True)

    class Meta:
        verbose_name = ("trip")
        verbose_name_plural = ("trips")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("trip_detail", kwargs={"pk": self.pk})
