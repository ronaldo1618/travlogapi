from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Traveler(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=75, null=True, blank=True)
    profile_pic = models.CharField(max_length=300, null=True)

    class Meta:
        verbose_name = ("traveler")
        verbose_name_plural = ("travelers")

    def __str__(self):
        return self.address

    def get_absolute_url(self):
        return reverse("traveler_detail", kwargs={"pk": self.pk})