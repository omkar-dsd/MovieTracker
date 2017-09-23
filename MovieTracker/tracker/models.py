from django.db import models

# Create your models here.

class UserWatched(models.Model):
    username = models.CharField(max_length=100)
    movie_id = models.IntegerField()
    movie_rating = models.IntegerField()
