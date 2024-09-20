from django.shortcuts import render, redirect
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

MY_API_KEY = 'AuahkYV8gyLfJjQW9d7B-W0JEVNbeeojSLFHbNC5vGp_SXfr2wj6nPb2aqbc3CRbmhOPxgAmDqwj08L2KH-GNa3fCTU3F7Jk2NMdVigSE6P72tYPVxy99q-SbWDsZnYx'

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
        'limit': 5
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

def restaurant_detail(request, restaurant_id):
    # Call the function to get restaurant details by its ID
    restaurant = get_restaurant_details_by_id(restaurant_id)
    review_form = ReviewForm()
    
    # Check if the restaurant was found
    if restaurant:
        return render(request, 'restaurants/detail.html', {'restaurant': restaurant, 'review_form': review_form})
    else:
        return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})
    

    # def restaurant_detail(request, restaurant_id):
#     # Call the function to get restaurant details by its ID
#     restaurant = get_restaurant_details_by_id(restaurant_id)
#     review_form = ReviewForm()
#     reviews = Review.objects.filter(restaurant__id=restaurant_id)

#         # Handle review form submission
#     if request.method == 'POST':
#         if request.user.is_authenticated:
#             form = ReviewForm(request.POST)
#             if form.is_valid():
#                 new_review = form.save(commit=False)
#                 new_review.restaurant_id = restaurant_id
#                 new_review.user = request.user  # Assign the current logged-in user
#                 new_review.save()
#                 return redirect('restaurant-detail', restaurant_id=restaurant_id)
#         else:
#             return redirect('login')  # Redirect to login if not authenticated
#     else:
#         form = ReviewForm()

#     # Check if the restaurant was found
#     if restaurant:
#         return render(request, 'restaurants/detail.html', {
#             'restaurant': restaurant,
#             'review_form': form,
#             'reviews': reviews
#         })
#     else:
#         return render(request, 'restaurants/detail.html', {'error': 'Restaurant not found'})