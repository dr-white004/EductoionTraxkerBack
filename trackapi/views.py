from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view ,permission_classes
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import status, generics
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from .models import User, Book, Chapter, Lesson
from .serializers import UserSerializer, BookSerializer,ChapterSerializer,LessonSerializer
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from django.db.models import Count
from rest_framework import permissions
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_405_METHOD_NOT_ALLOWED
from django.core.serializers import serialize






class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token
 
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
   
class MyTokenRefreshView(TokenRefreshView):
    pass


# Create your views here.
@api_view(['GET']) #for function based views decorator is needed
def displaything(request):
    routes = [
        'api/token'
        '/api/token/refresh'
    ]
    return Response(routes)



class CustomPasswordRecoveryView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        email = request.data.get('email')
        new_password = request.data.get('new_password')

        if not (username and email and new_password):
            return Response({'error': 'Username, email, and new password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(username=username, email=email).first()
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'Password reset successfully'}, status=status.HTTP_200_OK)



class UserCreateAPIView(CreateAPIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_book(request):
    if request.method == 'POST':
        data = request.data.copy()  # Access JSON data using request.data
        data['user'] = request.user.id
        serializer = BookSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Method not allowed'}, status=HTTP_405_METHOD_NOT_ALLOWED)



@method_decorator(csrf_exempt, name='dispatch')
class PresentBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        return Book.objects.filter(user=User.objects.get(pk=self.request.user.pk), category='present')


@method_decorator(csrf_exempt, name='dispatch')
class FutureBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        return Book.objects.filter(user=User.objects.get(pk=self.request.user.pk), category='future')


@method_decorator(csrf_exempt, name='dispatch')
class PastBooksAPIView(generics.ListAPIView):
    serializer_class = BookSerializer
    def get_queryset(self):
        return Book.objects.filter(user=User.objects.get(pk=self.request.user.pk), category='past')




class BookDetailView(APIView):
    def get_object(self, pk):
        try:
            return Book.objects.get(pk=pk)
        except Book.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        book = self.get_object(pk)
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        book = self.get_object(pk)
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



@api_view(['GET'])
def get_recommendations(request):

    # Get the current user
    user = request.user

    # Aggregate data to find most common genre and author for the current user
    most_common_genre = Book.objects.filter(user=user).values('genre').annotate(count=Count('genre')).order_by('-count').first()
    most_common_author = Book.objects.filter(user=user).values('author').annotate(count=Count('author')).order_by('-count').first()

    # Extract most common genre and author
    most_common_genre = most_common_genre['genre'] if most_common_genre else 'history'
    most_common_author = most_common_author['author'] if most_common_author else 'fyodor dostoevsky'

    # Send back the most common genre and author as JSON response
    return JsonResponse({'most_common_genre': most_common_genre, 'most_common_author': most_common_author})

class FavoriteBookAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        user = request.user
        book = Book.objects.get(id=pk)
        if user.favorite_books.exists():
            user.favorite_books.clear()
        user.favorite_books.add(book)
        serializer = BookSerializer(book)
        return Response({'message': 'Favorite book set successfully', 'favorite': serializer.data}, status=status.HTTP_200_OK)


def favorite_books(request):
    all_users = User.objects.all()
    favorite_books = []
    for user in all_users:
        favorite_books.extend(user.favorite_books.all())
        favorite_books_data = serialize('json', favorite_books)
    
    # Return the JSON response
    return JsonResponse({'favorite_books': favorite_books_data}, safe=False)

@api_view(['GET'])
def personal_favorite(request):
    user = request.user
    personal_favorite = []
    if user.favorite_books.exists():
        personal_favorite.extend(user.favorite_books.all())
        personal_favorite_data = serialize('json', personal_favorite)
        return JsonResponse({'personal_favorite': personal_favorite_data}, safe=False)
    
    # Return the JSON response
    return Response({'personal_favorite': ''}, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_chapter_with_lesson(request):
    data = request.data
    book_id = data.get('book_id')
    if not book_id:
        return Response({'error': 'Book ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    book = Book.objects.get(id=book_id)
    chapter_number = data.get('chapter_number')
    lesson_content = data.get('lesson_content')

    if not (chapter_number and lesson_content):
        return Response({'error': 'Chapter number and lesson content are required'}, status=status.HTTP_400_BAD_REQUEST)

    # Create chapter
    chapter = Chapter.objects.create(book=book, number=chapter_number)

    # Create lesson associated with the created chapter
    lesson = Lesson.objects.create(chapter=chapter, content=lesson_content)

    return Response({'message': 'Chapter and lesson created successfully', 'chapter_id': chapter.id, 'lesson_id': lesson.id}, status=status.HTTP_201_CREATED)

class ChapterAndLessonListView(generics.ListAPIView):
    serializer_class = LessonSerializer  # Use LessonSerializer for combined view

    def get_queryset(self):
        book_id = self.kwargs['book_id']  # Assuming book_id is passed as URL parameter
        chapters = Chapter.objects.filter(book=book_id).order_by('number')
        lessons = Lesson.objects.filter(chapter__in=chapters)
        return lessons  # Return lessons associated with chapters of the specified book

