from django.urls import path
from rhabitApp import views

urlpatterns = [
  path('', views.home_page, name = 'home_page'),
  path('login/', views.login_page, name = 'login_page'),
  path('signup/', views.signup_page, name = 'signup_page'),
  path('search/', views.search_page, name = 'search_page'),
  path('user/', views.user_page, name = 'user_page'),
  path('profile/', views.profile_page, name = 'profile_page'),
  path('aboutus/', views.about_us_page, name = 'about_us_page'),
]