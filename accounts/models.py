from django.contrib.auth.models import User
from django.db import models


class UserProfile(models.Model):
    date_of_birth = models.DateTimeField(null=True, blank=True)
    profile_image = models.ImageField(
        upload_to="profiles/",
        default='images/Anonymous-Avatar.png',
        null=True,
        blank=True,
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user)


class Subscribers(models.Model):
    emial = models.EmailField()
    subscribed = models.BooleanField(default=True)

    def __str__(self):
        return str(self.emial)
