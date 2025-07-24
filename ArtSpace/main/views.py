from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from accounts.models import ArtistProfile
from gallery.models import Artwork

# Create your views here.

def home_view(request: HttpRequest):
    artworks = Artwork.objects.all().order_by('-created_at')[:6]
    return render(request, 'main/home.html', {'artworks': artworks})


def artists_list_view(request: HttpRequest):
    artists = ArtistProfile.objects.select_related('user').all()
    return render(request, 'main/artists.html', {'artists': artists})


def contact_view(request: HttpRequest):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')
        messages.success(request, 'Thank you for contacting us! We will get back to you soon.')
        return redirect('main:contact')
    return render(request, 'main/contact.html')


