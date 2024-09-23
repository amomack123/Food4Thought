from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Restaurant, Review
from .forms import ReviewForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Yelp_API import get_restaurant_details_by_id
import requests

MY_API_KEY = '4Z2h2Gios3QOnYb-UZ-qDhMs8udoVoB5OTPLFdD13gtsxCHEWBVjWDuuj6zJPO4l5FfnGHJfpxbaqYCKRrgXzydXRYKxfK-nZww7S3mfnNqfpMhEuBxKTdMOMF_sZnYx'
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % MY_API_KEY}

class Home(LoginView):
    template_name = 'home.html'  

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

def restaurant_index(request):
    location = ""
    category = ""
    if request.method == "POST":
        location = request.POST.get('location')
        category = request.POST.get('category')

    params = {
        'location': location,
        'term': category,
        'limit': 10
    }

    response = requests.get(url, headers=headers, params=params)
    restaurants = response.json().get('businesses', [])

    return render(request, 'restaurants/index.html', {'restaurants': restaurants})

@login_required
def add_review(request, restaurant_id):
    print(restaurant_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.restaurant_id = restaurant_id
        new_review.save()
    return redirect('restaurant-detail', {'restaurant_id': restaurant_id})

# Adding restaurant to favorites
@login_required
def add_to_favorites(request, restaurant_id):
    favorite, created = Favorites.objects.get_or_create(user=request.user, restaurant_id=restaurant_id)
    # restaurant = get_object_or_404(Restaurant, yelp_id=restaurant_id)
    # request.user.favorite_restaurants.add(restaurant)
    return redirect('favorites-list')

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

def restaurant_detail(request, restaurant_id):
    # Call the function to get restaurant details by its ID
    restaurant = get_restaurant_details_by_id(restaurant_id)
    review_form = ReviewForm()

    # params = {
    #     'id': restaurant_id
    # }

    # response = requests.get(url, headers=headers, params=params)
    # restaurant_query = response.json().get('businesses', [])

    # print (restaurant_query)

    # new_restaurant = Restaurant
    # new_restaurant.yelp_id = restaurant_id
    # new_restaurant.save()
    
    # Check if the restaurant was found
    if restaurant:
        return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'review_form': review_form , 'restaurant_id': restaurant_id})
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})

@login_required
def favorites_list(request):
    favorites = Favorites.objects.filter(user=request.user) # get the user's favorite restaurants

    return render(request, 'restaurants/favorites_list.html', {'favorites': favorites})
