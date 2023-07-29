from django.urls import path
from .views import *
urlpatterns = [
    path('',HomePage.as_view(), name='index_page'),
    path('register/',RegisterUser.as_view(), name='register_user'),
    path('login/',LoginUser.as_view(), name='login_user'),
    path('logout/',logout_user, name="logout"),
    path('profile/', UserProfile.as_view(), name="user_profile"),
    path('edit_profile', EditProfile.as_view(), name="edit_profile"),
    path('category/<slug:cat_slug>/', CategoryProduct.as_view(), name="category_product"),
]
