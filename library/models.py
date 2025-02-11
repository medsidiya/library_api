from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Author(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    name = models.CharField(max_length=200)
    role = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    title = models.CharField(max_length=500)
    isbn = models.CharField(max_length=20, blank=True, null=True)
    isbn13 = models.CharField(max_length=20, blank=True, null=True)
    language = models.CharField(max_length=50, blank=True, null=True)
    average_rating = models.FloatField(blank=True, null=True)
    ratings_count = models.IntegerField(blank=True, null=True)
    text_reviews_count = models.IntegerField(blank=True, null=True)
    publication_date = models.CharField(max_length=50, blank=True, null=True)
    publisher = models.CharField(max_length=200, blank=True, null=True)
    num_pages = models.IntegerField(blank=True, null=True)
    image_url = models.URLField(blank=True, null=True)
    authors = models.ManyToManyField(Author, related_name='books')

    def __str__(self):
        return self.title
    
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey('Book', on_delete=models.CASCADE, related_name='favorites')

    class Meta:
        unique_together = ('user', 'book')  # Ensure a user can't favorite the same book twice

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"