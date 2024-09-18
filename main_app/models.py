from django.db import models

class Restaurant(models.Model):
    yelp_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.name
