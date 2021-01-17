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
