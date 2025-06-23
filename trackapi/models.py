from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse


User = get_user_model()

class Book(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    pages = models.IntegerField()
    genre = models.CharField(max_length=100)
    description = models.TextField('')
    category = models.CharField(max_length=10, choices=(('past', 'Past'), ('present', 'Present'), ('future', 'Future')))
    favorite_of = models.ForeignKey(User, related_name='favorite_books', on_delete=models.SET_NULL, null=True, blank=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail', args=[str(self.id)])

class Chapter(models.Model):
    book = models.ForeignKey(Book, related_name='chapters', on_delete=models.CASCADE)
    number = models.IntegerField()

    def __str__(self):
        return f"{self.book.title} - Chapter {self.number}"

class Lesson(models.Model):
    chapter = models.ForeignKey(Chapter, related_name='lessons', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return f"{self.chapter.book.title} - Chapter {self.chapter.number} - Lesson"


