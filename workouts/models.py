from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

class WorkoutSession(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200,blank=True)
    location = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    workout_date = models.DateTimeField('workout date')

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        default=1,on_delete=models.CASCADE,
    )

    attendees = models.ManyToManyField(
        User,
        related_name="%(app_label)s_%(class)s_related",
    )

    def __str__(self):
        return self.name
