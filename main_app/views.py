from django.shortcuts import render
from .models import Restaurant

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def restaurant_index(request):
    restaurants = Restaurant.objects.all()
    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})