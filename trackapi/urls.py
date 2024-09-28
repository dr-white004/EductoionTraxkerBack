from . import views
from django.urls import path
from .views import MyTokenObtainPairView,  UserCreateAPIView, BookDetailView,get_recommendations,personal_favorite, FavoriteBookAPIView,favorite_books, PresentBooksAPIView,FutureBooksAPIView,PastBooksAPIView,create_book, create_chapter_with_lesson, ChapterAndLessonListView,CustomPasswordRecoveryView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path ('', views.displaything, name='displaything'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', UserCreateAPIView.as_view(), name='user_create'),
    path('books/', create_book, name='book-create'),
    path('present-books/',PresentBooksAPIView.as_view(), name='present-books'),
    path('future-books/',FutureBooksAPIView.as_view(), name='future-books'),
    path('past-books/',PastBooksAPIView.as_view(), name='past-books'),
    path('detail-books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('recommend-books/', get_recommendations, name= 'get_recommendations'),
    path('favorite-book/<int:pk>/', FavoriteBookAPIView.as_view(), name='FavoriteBook'),
    path('favorite-books/',favorite_books, name= 'favorite_books'),
    path('personal-favorite/',personal_favorite, name= 'personal_favorite'),
    path('create-chapter-with-lesson/', create_chapter_with_lesson, name='create_chapter_with_lesson'),
    path('chapters-and-lessons/<int:book_id>/', ChapterAndLessonListView.as_view(), name='chapter_and_lesson_list'),
    path('password-recovery/', CustomPasswordRecoveryView.as_view(), name='password_recovery'),
   
   
]




 

