# content/serializers.py

from rest_framework import serializers
from .models import Subject, Chapter, Lesson, Exercise, Question, Answer

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'answer_text', 'is_correct', 'explanation']

class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True)
    
    class Meta:
        model = Question
        fields = ['id', 'question_text', 'question_type', 'media_url', 'media_file', 'points', 'order_num', 'answers']

class ExerciseSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    
    class Meta:
        model = Exercise
        fields = ['id', 'title', 'description', 'difficulty_level', 'points', 'time_limit', 'slug', 'questions']

class LessonSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True, read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content', 'content_type', 'media_url', 'media_file', 'duration', 
                 'order_num', 'is_downloadable', 'slug', 'created_at', 'updated_at', 'exercises']

class ChapterSerializer(serializers.ModelSerializer):
    lessons = LessonSerializer(many=True, read_only=True)
    
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'order_num', 'slug', 'created_at', 'updated_at', 'lessons']

class SubjectSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True, read_only=True)
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'icon', 'slug', 'created_at', 'updated_at', 'chapters']

# Serializers simplifiés pour les listes
class SubjectListSerializer(serializers.ModelSerializer):
    chapters_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'icon', 'slug', 'chapters_count']
    
    def get_chapters_count(self, obj):
        return obj.chapters.count()

class ChapterListSerializer(serializers.ModelSerializer):
    lessons_count = serializers.SerializerMethodField()
    subject_name = serializers.CharField(source='subject.name', read_only=True)
    
    class Meta:
        model = Chapter
        fields = ['id', 'title', 'description', 'order_num', 'slug', 'subject_name', 'lessons_count']
    
    def get_lessons_count(self, obj):
        return obj.lessons.count()

class LessonListSerializer(serializers.ModelSerializer):
    chapter_title = serializers.CharField(source='chapter.title', read_only=True)
    subject_name = serializers.CharField(source='chapter.subject.name', read_only=True)
    
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'content_type', 'duration', 'order_num', 'is_downloadable', 
                 'slug', 'chapter_title', 'subject_name']