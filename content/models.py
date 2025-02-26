# content/models.py

from django.db import models
from django.utils.text import slugify

class Subject(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='subjects/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name

class Chapter(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    order_num = models.IntegerField()
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_num']
        unique_together = ('subject', 'slug')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.subject.name} - {self.title}"

class Lesson(models.Model):
    CONTENT_TYPE_CHOICES = (
        ('text', 'Texte'),
        ('video', 'Vidéo'),
        ('audio', 'Audio'),
        ('interactive', 'Interactif'),
    )
    
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    content = models.TextField()
    content_type = models.CharField(max_length=50, choices=CONTENT_TYPE_CHOICES, default='text')
    media_url = models.URLField(null=True, blank=True)
    media_file = models.FileField(upload_to='lessons/', null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True, help_text="Durée en minutes")
    order_num = models.IntegerField()
    is_downloadable = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_num']
        unique_together = ('chapter', 'slug')
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.chapter.subject.name} - {self.chapter.title} - {self.title}"

class Exercise(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='exercises')
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    difficulty_level = models.IntegerField(choices=[(i, i) for i in range(1, 6)], default=1)
    points = models.IntegerField(default=10)
    time_limit = models.IntegerField(null=True, blank=True, help_text="Temps limite en secondes")
    slug = models.SlugField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.lesson.title} - {self.title}"

class Question(models.Model):
    QUESTION_TYPE_CHOICES = (
        ('multiple_choice', 'Choix multiple'),
        ('true_false', 'Vrai ou Faux'),
        ('fill_blank', 'À compléter'),
        ('matching', 'Association'),
        ('essay', 'Rédaction'),
    )
    
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    question_type = models.CharField(max_length=50, choices=QUESTION_TYPE_CHOICES, default='multiple_choice')
    media_url = models.URLField(null=True, blank=True)
    media_file = models.FileField(upload_to='questions/', null=True, blank=True)
    points = models.IntegerField(default=1)
    order_num = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order_num']
    
    def __str__(self):
        return f"Question {self.order_num}: {self.question_text[:50]}..."

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)
    explanation = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.answer_text[:50]}... ({'Correct' if self.is_correct else 'Incorrect'})"