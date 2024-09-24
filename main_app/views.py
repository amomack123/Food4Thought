from django.shortcuts import render, redirect, get_object_or_404
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
# from django.http import JsonResponse
from django.contrib import messages
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

@login_required
def favorites_list(request):
    favorites = request.user.favorite_restaurants.all()
    categories = favorites.values_list('category', flat=True).distinct()


    return render(request, 'restaurants/favorites_list.html', {'favorites': favorites, 'categories': categories})

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
                'category': restaurant_data.get('category', 'Unknown'),
                'image_url': restaurant_data.get('image_url', 'default-image-url')
            }
        )
        return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'restaurant_id': restaurant_id})
    
    # If no restaurant data is found, return a 404 page
    return render(request, '404.html', status=404)
    
def save_restaurant(request, restaurant_id):
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
        
        request.user.favorite_restaurants.add(restaurant)

        messages.success(request, 'Restaurant saved to your favorites!')
        return redirect('restaurant-detail', restaurant_id=restaurant_id)
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})
    

def unfavorite_restaurant(request, restaurant_id):
    if request.user.is_authenticated:

        restaurant = get_object_or_404(Restaurant, yelp_id=restaurant_id)
        
        request.user.favorite_restaurants.remove(restaurant)
        
        messages.success(request, 'Restaurant removed from your favorites!')
        
        return redirect('favorites-list')
    
    messages.warning(request, 'You need to be logged in to unfavorite restaurants.')
    return redirect('login')
    

def review_update(request, restaurant_id):
    restaurant = Restaurant.objects.get(yelp_id=restaurant_id)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('restaurant-detail', restaurant_id=restaurant_id)
    else:
        form = ReviewForm(instance=review)
        
    reviews = Review.objects.filter(restaurant=restaurant)
    
    return render(request, 'restaurants/review.html', { 'form': form, 'restaurant': restaurant, 'restaurant_id': restaurant_id, 'reviews': reviews, 'edit_review_id': review_id} )

@login_required
def review_delete(request, restaurant_id, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    restaurant = get_restaurant_details_by_id(restaurant_id)
    reviews = Review.objects.filter(restaurant=restaurant)
    
    if request.method == 'POST':
        review.delete()
        return redirect('restaurant-detail', restaurant_id=restaurant_id)
        
    
    return render(request, 'restaurants/delete.html', { 'restaurant': restaurant, 'restaurant_id': restaurant_id, 'reviews': reviews, 'delete_review_id': review_id })
    
