from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Restaurant, Review
from .forms import ReviewForm
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from Yelp_API import get_restaurant_details_by_id
import requests

MY_API_KEY = 'AuahkYV8gyLfJjQW9d7B-W0JEVNbeeojSLFHbNC5vGp_SXfr2wj6nPb2aqbc3CRbmhOPxgAmDqwj08L2KH-GNa3fCTU3F7Jk2NMdVigSE6P72tYPVxy99q-SbWDsZnYx'
url = 'https://api.yelp.com/v3/businesses/search'
headers = {'Authorization': 'bearer %s' % MY_API_KEY}

class Home(LoginView):
    template_name = 'home.html'  

def home(request):
    return render(request, 'base.html')

def about(request):
    return render(request, 'about.html')

@login_required
def favorites_list(request):
    favorites = request.user.favorite_restaurants.all()

    return render(request, 'restaurants/favorites_list.html', {'favorites': favorites})

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
    restaurant = Restaurant.objects.get(yelp_id=restaurant_id)
    form = ReviewForm(request.POST)
    if form.is_valid():
        new_review = form.save(commit=False)
        new_review.restaurant = restaurant
        new_review.user = request.user
        new_review.save()
        print(f"Review saved: {new_review}")
    else:
        print("Form is not valid")
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

def restaurant_detail(request, restaurant_id):
    # Call the function to get restaurant details by its ID
    restaurant_data = get_restaurant_details_by_id(restaurant_id)
    
    if restaurant_data:
        restaurant, created = Restaurant.objects.get_or_create(
            yelp_id=restaurant_id,
            defaults={
                'name': restaurant_data['name'],
                'location': restaurant_data['location'],
                'category': restaurant_data.get('category'),
                'image_url': restaurant_data.get('image_url')
            }
        )
        
        if created:
            restaurant.save()
            
        review_form = ReviewForm()
        reviews = Review.objects.filter(restaurant=restaurant)
        
    
    # Check if the restaurant was found
    if restaurant:
        return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'review_form': review_form, 'reviews': reviews, 'restaurant_id': restaurant_id})
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})
    
def save_restaurant(request, restaurant_id):
    restaurant_data = get_restaurant_details_by_id(restaurant_id)
    
    if restaurant_data:
        restaurant, created = Restaurant.objects.get_or_create(
            yelp_id=restaurant_id,
            defaults={
                'name': restaurant_data['name'],
                'location': restaurant_data['location'],
                'category': restaurant_data['category'],
                'image_url': restaurant_data['image_url']
            }
        )
        
        request.user.favorite_restaurants.add(restaurant)
        
        
        return redirect(reverse('favorites-list'))
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})
    

def review_update(request):
    restaurant = Restaurant.objects.get(yelp_id=restaurant_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('restaurant-detail', restaurant)
    