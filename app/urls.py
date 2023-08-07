from django.urls import path
from .views import *
urlpatterns = [
    path('',HomePage.as_view(), name='index_page'),
    path('register/',RegisterUser.as_view(), name='register_user'),
    path('login/',LoginUser.as_view(), name='login_user'),
    path('logout/',logout_user, name="logout"),
    path('profile/', UserProfile.as_view(), name="user_profile"),
    path('profile/order_history', OrderHistory.as_view(), name='order_history'),
    path('edit_profile/', EditProfile.as_view(), name="edit_profile"),
    path('about_user/', AboutAccount.as_view(), name='about_user'),
    path('category/<slug:cat_slug>/', CategoryProduct.as_view(), name="category_product"),
    path('cart/', CartPage.as_view(), name="user_cart"),
    path('cart/add_ajax/<int:product_id>/<int:item_quantity>/', add_to_cart, name='add_to_cart_ajax'),
    path('cart/remove_ajax/<int:item_id>/', remove_from_cart, name="remove_from_cart_ajax"),
    path('cart/clear_cart', clear_cart, name="clear_cart"),
    path('cart/update_quantity/<int:item_id>/<int:new_quantity>/', update_quantity, name='update_quantity'),
    path('cart/buy_items', buy_cart_items, name="buy_cart_items"),
]
