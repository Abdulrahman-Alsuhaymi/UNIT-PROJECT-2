from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Artwork(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='artworks/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    artist = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artworks')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name='liked_artworks')

    def __str__(self):
        return self.title

class Comment(models.Model):
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} on {self.artwork.title}'

class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    artworks = models.ManyToManyField(Artwork, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}'s Cart"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    artwork = models.ForeignKey(Artwork, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.artwork.title} in {self.cart.user.username}'s Cart"
