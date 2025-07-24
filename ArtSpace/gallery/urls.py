from django.urls import path
from . import views

app_name = "gallery"

urlpatterns = [
    path('', views.gallery_view, name="gallery_view"),
    path('art/<int:artwork_id>/', views.artwork_detail_view, name="artwork_detail"),
    path('art/<int:artwork_id>/add_comment/', views.add_comment_view, name="add_comment"),
    path('art/<int:artwork_id>/like/', views.toggle_like_view, name="toggle_like"),
    path('artists/<str:username>/', views.artist_profile_view, name="artist_profile"),
    path('wishlist/', views.wishlist_view, name="wishlist"),
    path('wishlist/add/<int:artwork_id>/', views.add_to_wishlist_view, name="add_to_wishlist"),
    path('wishlist/remove/<int:artwork_id>/', views.remove_from_wishlist_view, name="remove_from_wishlist"),
    path('search/', views.search_artworks_view, name="search_artworks"),
    path('cart/', views.cart_view, name="cart"),
    path('cart/add/<int:artwork_id>/', views.add_to_cart_view, name="add_to_cart"),
    path('cart/remove/<int:item_id>/', views.remove_from_cart_view, name="remove_from_cart"),
    path('checkout/', views.checkout_view, name="checkout"),
] 