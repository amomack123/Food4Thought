from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Restaurant
from .forms import ReviewForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Yelp_API import get_restaurant_details_by_id
import requests

MY_API_KEY = 'Gg65rpmjeX_dtHi23G6_dX9GrUnRI8i-p5x4SSTcmyUi8C2pElUS-bvsn2nbuIrPc1QvfxV9lMxvGeVGmkeI3D8b8tIw7CfTqdvr36sXpCtPSIjMO493ccuH5QHqZnYx'

class Home(LoginView):
    template_name = 'home.html'

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def restaurant_index(request):
    url = 'https://api.yelp.com/v3/businesses/search'
    headers = {'Authorization': 'bearer %s' % MY_API_KEY}
    params = {
        'location': 'San Francisco',
        'term': 'restaurants',
        'limit': 10
    }

# def restaurant_detail(request, restaurant_id):
#     restaurant = Restaurant.objects.get(id=restaurant_id)
#     review_form = ReviewForm()
#     return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'review_form': review_form})

def restaurant_detail(request, restaurant_id):
    # Call the function to get restaurant details by its ID
    restaurant = get_restaurant_details_by_id(restaurant_id)
    review_form = ReviewForm()
    
    # Check if the restaurant was found
    if restaurant:
        return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'review_form': review_form})
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})

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

@login_required
def add_review(request, restaurant_id):
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.restaurant_id = restaurant_id
        new_review.save()
    return redirect('restaurant-detail', restaurant_id=restaurant_id)

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('restaurant-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)