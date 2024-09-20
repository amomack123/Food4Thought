from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('restaurants/', views.restaurant_index, name='restaurant-index'),
    path('restaurants/my-favorites/', views.favorites_list, name='favorites-list'),  # Ensure this is added
    path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('restaurants/<str:restaurant_id>/add-review/', views.add_review, name='add-review'),
    path('restaurants/<str:restaurant_id>/add_to_favorites/', views.add_to_favorites, name='add-to-favorites'),
    # path('restaurants/<str:restaurant_id>/favorites-list/', views.favorites_list, name='favorites-list'),
    path('accounts/signup/', views.signup, name='signup'),
    # path('', views.Home.as_view(), name='home'),
    # path('about/', views.about, name='about'),
    # path('restaurants/', views.restaurant_index, name='restaurant-index'),
    # path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    # path('restaurants/<str:restaurant_id>/add-review/', views.add_review, name='add-review'),
    # path('restaurants/<str:restaurant_id>/favorite/', views.favorite_restaurant, name='favorite-restaurant'),
    # path('accounts/signup/', views.signup, name='signup'),
]