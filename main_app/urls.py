from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('restaurants/', views.restaurant_index, name='restaurant-index'),
    path('restaurants/my-favorites/', views.favorites_list, name='favorites-list'),
    path('restaurants/my-favorites/<str:restaurant_id>/', views.save_restaurant, name='save-restaurant'),
    path('restaurants/<str:restaurant_id>/add-review/', views.add_review, name='add-review'),
    path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('accounts/signup/', views.signup, name='signup'),
    path('restaurants/unfavorite/<str:restaurant_id>/', views.unfavorite_restaurant, name='unfavorite_restaurant'),
    path('restaurants/<str:restaurant_id>/review/<int:review_id>/', views.review_update, name='review-update'),
]