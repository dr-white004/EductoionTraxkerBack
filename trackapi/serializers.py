from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Book, Chapter, Lesson

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = get_user_model().objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user



class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chapter
        fields = ['id', 'book', 'number']

class LessonSerializer(serializers.ModelSerializer):
    chapter = serializers.SerializerMethodField()

    def get_chapter(self, obj):
        return ChapterSerializer(obj.chapter).data  # Assuming you have a ChapterSerializer

    class Meta:
        model = Lesson
        fields = ['id', 'content', 'chapter']
