from django.db import models
from django.contrib.auth.models import User

STARS = (
    ('1', 1),
    ('2', 2),
    ('3', 3),
    ('4', 4),
    ('5', 5)
)

class Restaurant(models.Model):
    yelp_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100, null=True)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100, null=True, blank=True)
    image_url = models.CharField(max_length=100, null=True, blank=True)
    favorited_by = models.ManyToManyField(User, related_name='favorite_restaurants', blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)


    def __str__(self):
        return self.name or f"Restaurant {self.yelp_id}"

class Review(models.Model):
    stars = models.CharField(max_length=1, choices=STARS)
    comment = models.TextField(max_length=250)
    restaurant = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return f"{self.stars()}"