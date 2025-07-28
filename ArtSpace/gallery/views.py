from django.shortcuts import render, redirect
from django.http import HttpRequest
from .models import *
from accounts.models import ArtistProfile
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.

def gallery_view(request: HttpRequest):
    artworks = Artwork.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    category_id = request.GET.get('category', '')
    if category_id:
        artworks = artworks.filter(category_id=category_id)
    
    return render(request, 'gallery/gallery.html', {
        'artworks': artworks,
        'categories': categories,
        'selected_category': category_id
    })

def artwork_detail_view(request: HttpRequest, artwork_id: int):
    artwork = Artwork.objects.get(id=artwork_id)
    comments = artwork.comments.all()
    in_wishlist = False
    if request.user.is_authenticated:
        wishlist, created = Wishlist.objects.get_or_create(user=request.user)
        in_wishlist = artwork in wishlist.artworks.all()
    return render(request, 'gallery/artwork_detail.html', {'artwork': artwork,'comments': comments,'in_wishlist': in_wishlist
    })

def add_comment_view(request: HttpRequest, artwork_id: int):
    if request.method == "POST":
        artwork = Artwork.objects.get(pk=artwork_id)
        text = request.POST.get("text", "")
        if text and request.user.is_authenticated:
            Comment.objects.create(artwork=artwork, user=request.user, text=text)
    return redirect("gallery:artwork_detail", artwork_id=artwork_id)

def artist_profile_view(request: HttpRequest, username: str):
    user = User.objects.get(username=username)
    profile = ArtistProfile.objects.get(user=user)
    artworks = Artwork.objects.filter(artist=user)
    categories = artworks.values_list('category__name', flat=True).distinct()
    return render(request, 'gallery/artist_profile.html', {'profile': profile,'artworks': artworks,'categories': categories})

def wishlist_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    return render(request, 'gallery/wishlist.html', {'wishlist': wishlist})


def add_to_wishlist_view(request: HttpRequest, artwork_id: int):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    wishlist.artworks.add(artwork)
    return redirect('gallery:wishlist')


def remove_from_wishlist_view(request: HttpRequest, artwork_id: int):
    wishlist, created = Wishlist.objects.get_or_create(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    wishlist.artworks.remove(artwork)
    return redirect('gallery:wishlist')

def search_artworks_view(request: HttpRequest):
    artworks = Artwork.objects.all()
    categories = Category.objects.all()
    artists = User.objects.filter(artworks__isnull=False).distinct()

    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")
    artist_username = request.GET.get("artist", "")
    order_by = request.GET.get("order_by", "")

    if search and len(search) >= 3:
        artworks = artworks.filter(title__contains=search)
    if category_id:
        artworks = artworks.filter(category_id=category_id)
    if artist_username:
        artworks = artworks.filter(artist__username=artist_username)
    if order_by:
        if order_by == "price":
            artworks = artworks.order_by("price")
        elif order_by == "created_at":
            artworks = artworks.order_by("-created_at")

    return render(request, "gallery/search_artworks.html", {
        "artworks": artworks,
        "categories": categories,
        "artists": artists,
        "search": search,
        "selected_category": category_id,
        "selected_artist": artist_username,
        "order_by": order_by,
    })

def cart_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('artwork')
    total = sum(item.artwork.price for item in items)
    return render(request, 'gallery/cart.html', {'cart': cart, 'items': items, 'total': total})

def add_to_cart_view(request: HttpRequest, artwork_id: int):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    artwork = Artwork.objects.get(id=artwork_id)
    CartItem.objects.get_or_create(cart=cart, artwork=artwork)
    return redirect('gallery:cart')

def remove_from_cart_view(request: HttpRequest, item_id: int):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    CartItem.objects.filter(id=item_id, cart__user=request.user).delete()
    return redirect('gallery:cart')

def checkout_view(request: HttpRequest):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    cart, created = Cart.objects.get_or_create(user=request.user)
    items = cart.items.select_related('artwork')
    total = sum(item.artwork.price for item in items)
    if request.method == 'POST':
        cart.items.all().delete()
        messages.success(request, 'Thank you for your purchase!')
        return redirect('gallery:cart')
    return render(request, 'gallery/checkout.html', {'cart': cart, 'items': items, 'total': total})

def toggle_like_view(request: HttpRequest, artwork_id: int):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    artwork = Artwork.objects.get(id=artwork_id)
    if request.user in artwork.likes.all():
        artwork.likes.remove(request.user)
    else:
        artwork.likes.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'gallery:gallery_view'))
