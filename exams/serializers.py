# exams/serializers.py

from rest_framework import serializers
from .models import Exam, ExamExercise, ExamResult
from content.serializers import ExerciseSerializer
from accounts.serializers import UserSerializer

class ExamExerciseSerializer(serializers.ModelSerializer):
    exercise_details = ExerciseSerializer(source='exercise', read_only=True)
    
    class Meta:
        model = ExamExercise
        fields = ['id', 'exercise', 'weight', 'order', 'exercise_details']

class ExamSerializer(serializers.ModelSerializer):
    exam_exercises = ExamExerciseSerializer(many=True, read_only=True)
    created_by_details = UserSerializer(source='created_by', read_only=True)
    total_exercises = serializers.SerializerMethodField()
    total_points = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'exam_type', 'time_limit', 'passing_score', 
                 'created_by', 'created_by_details', 'year', 'is_public', 'slug', 'created_at', 
                 'updated_at', 'exam_exercises', 'total_exercises', 'total_points']
    
    def get_total_exercises(self, obj):
        return obj.exercises.count()
    
    def get_total_points(self, obj):
        return obj.total_points

class ExamListSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField()
    total_exercises = serializers.SerializerMethodField()
    
    class Meta:
        model = Exam
        fields = ['id', 'title', 'exam_type', 'time_limit', 'passing_score', 'year', 
                 'is_public', 'slug', 'created_at', 'created_by_name', 'total_exercises']
    
    def get_created_by_name(self, obj):
        if obj.created_by:
            return obj.created_by.get_full_name()
        return None
    
    def get_total_exercises(self, obj):
        return obj.exercises.count()

class ExamResultSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.get_full_name', read_only=True)
    exam_title = serializers.CharField(source='exam.title', read_only=True)
    score_percentage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ExamResult
        fields = ['id', 'student', 'exam', 'score', 'max_score', 'completion_time', 'passed',
                 'attempt_number', 'completed_at', 'feedback', 'student_name', 'exam_title', 
                 'score_percentage']
        read_only_fields = ['student_name', 'exam_title', 'score_percentage']