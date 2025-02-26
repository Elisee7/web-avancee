# progress/serializers.py

from rest_framework import serializers
from .models import StudentProgress, ExerciseResult, StudentAnswer
from content.serializers import LessonSerializer, ExerciseSerializer, QuestionSerializer
from accounts.serializers import UserSerializer

class StudentProgressSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    lesson_details = LessonSerializer(source='lesson', read_only=True)
    
    class Meta:
        model = StudentProgress
        fields = ['id', 'student', 'lesson', 'completion_status', 'completion_date', 
                 'last_accessed', 'time_spent', 'student_details', 'lesson_details']

class StudentAnswerSerializer(serializers.ModelSerializer):
    question_details = QuestionSerializer(source='question', read_only=True)
    
    class Meta:
        model = StudentAnswer
        fields = ['id', 'question', 'answer_text', 'is_correct', 'points_earned', 'question_details']

class ExerciseResultSerializer(serializers.ModelSerializer):
    student_details = UserSerializer(source='student', read_only=True)
    exercise_details = ExerciseSerializer(source='exercise', read_only=True)
    answers = StudentAnswerSerializer(many=True, read_only=True)
    score_percentage = serializers.FloatField(read_only=True)
    
    class Meta:
        model = ExerciseResult
        fields = ['id', 'student', 'exercise', 'score', 'max_score', 'completion_time', 
                 'attempt_number', 'completed_at', 'score_percentage', 
                 'student_details', 'exercise_details', 'answers']

class StudentProgressSummarySerializer(serializers.Serializer):
    student = serializers.IntegerField()
    student_name = serializers.CharField()
    total_lessons = serializers.IntegerField()
    completed_lessons = serializers.IntegerField()
    in_progress_lessons = serializers.IntegerField()
    not_started_lessons = serializers.IntegerField()
    completion_percentage = serializers.FloatField()
    total_time_spent = serializers.IntegerField()
    
#    def to_representation(self, instance):
#        data = super().to_representation(instance)
#        # Convertir le temps passé de secondes en heures et minutes
#        total_seconds = data['total_time_spent']
#        hours = total_seconds // 3

def to_representation(self, instance):
    data = super().to_representation(instance)
    total_seconds = data['total_time_spent']
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    data['total_time_spent_formatted'] = f"{hours}h {minutes}min"
    return data