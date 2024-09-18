from django.shortcuts import render

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

class Restaurant:
    def __init__(self, yelp_id, name, location, category, image_url, favorited=False):
        self.yelp_id = yelp_id
        self.name = name
        self.location = location
        self.category = category
        self.image_url = image_url
        self.favorited = favorited

restaurants = [
    Restaurant(1, 'Dennys', 'Los Angeles', 'Diner', 'www.google.com'),
    Restaurant(2, 'McDonalds', 'Seattle', 'Fast Food', 'www.bing.com'),
    Restaurant(3, 'Innout', 'New York', 'Fast Food', 'www.yahoo.com'),
]

def restaurant_index(request):
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})
