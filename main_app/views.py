from django.shortcuts import render
from django.views.generic.edit import CreateView
from .models import Restaurant
import requests

MY_API_KEY = 'Gg65rpmjeX_dtHi23G6_dX9GrUnRI8i-p5x4SSTcmyUi8C2pElUS-bvsn2nbuIrPc1QvfxV9lMxvGeVGmkeI3D8b8tIw7CfTqdvr36sXpCtPSIjMO493ccuH5QHqZnYx'

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

# def restaurant_index(request):
#     restaurants = Restaurant.objects.all()
#     return render(request, 'restaurants/index.html', {'restaurants': restaurants})

def restaurant_detail(request, restaurant_id):
    restaurant = Restaurant.objects.get(id=restaurant_id)
    return render(request, 'restaurants/detail.html', {'restaurant': restaurant})

def restaurant_index(request):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % MY_API_KEY}
    params = {
        'location': 'San Francisco',
        'term': 'restaurants',
        'limit': 10
    }

    response = requests.get(url, headers=headers, params=params)
    restaurants = response.json().get('businesses', [])

    return render(request, 'restaurants/index.html', {'restaurants': restaurants})