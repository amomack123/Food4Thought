from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('restaurants/', views.restaurant_index, name='restaurant-index'),
    # path('restaurants/<int:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('restaurants/<str:restaurant_id>/', views.restaurant_detail, name='restaurant-detail'),
    path('restaurants/<int:restaurant_id>/add-review/', views.add_review, name='add-review'),
    path('accounts/signup/', views.signup, name='signup'),
]