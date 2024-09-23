from django.db import models
from django.urls import reverse
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
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    image_url = models.CharField(max_length=100)
    favorited = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('restaurant-detail', kwargs={'restaurant_id': self.id})

class Review(models.Model):
    stars = models.CharField(max_length=1, choices=STARS)
    comment = models.TextField(max_length=250)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.stars()}"