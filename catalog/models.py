from django.db import models

# Create your models here.

from django.urls import reverse  # To generate URLS by reversing URL patterns

class Book(models.Model):
    """Model representing a book. """
    title = models.CharField(max_length=50, default=' ')
    author = models.CharField(max_length=100, default=' ')
    bookcase = models.CharField(max_length=3, default=' ')
    shelf = models.CharField(max_length=3, default=' ')
    genre = models.CharField(max_length=50, default=' ')
    language = models.CharField(max_length=50, default=' ')
    format = models.CharField(max_length=50, default=' ')
    other = models.CharField(max_length=100, blank=True)

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])

    display_genre.short_description = 'Genre'

    def get_absolute_url(self):
        """Returns the url to access a particular book instance."""
        return reverse('book-detail', args=[str(self.id)])

    def __str__(self):
        """String for representing the Model object."""
        return self.title
