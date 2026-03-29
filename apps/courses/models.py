from django.db import models

class Field(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="e.g. Programming, Science")
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    field = models.ForeignKey(Field, on_delete=models.CASCADE, related_name='categories')
    name = models.CharField(max_length=100, help_text="e.g. Frontend, Backend")
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        return f"{self.field.name} -> {self.name}"

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    # Migrated to ForeignKey hierarchy:
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='courses')
    legacy_category = models.CharField(max_length=100, blank=True, null=True, help_text="Old flat category")
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="Tashqi havola (YouTube / Vimeo)")
    video_file = models.FileField(upload_to="videos/courses/", blank=True, null=True, help_text="Kompyuterdan MP4 video yuklash")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    title = models.CharField(max_length=255)
    video_url = models.URLField(max_length=500, blank=True, null=True, help_text="Tashqi havola")
    video_file = models.FileField(upload_to="videos/lessons/", blank=True, null=True, help_text="Kompyuterdan MP4 video yuklash")
    order = models.PositiveIntegerField(default=1)
    transcript = models.TextField(blank=True, null=True, help_text="Used for AI test generation")

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.course.title} - {self.title}"

class Quiz(models.Model):
    lesson = models.OneToOneField(Lesson, on_delete=models.CASCADE, related_name='quiz')
    title = models.CharField(max_length=255, default="Lesson Quiz")
    passing_score = models.IntegerField(default=70)
    
    def __str__(self):
        return f"Quiz for {self.lesson.title}"

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    text = models.TextField()
    option_a = models.CharField(max_length=200)
    option_b = models.CharField(max_length=200)
    option_c = models.CharField(max_length=200, blank=True, null=True)
    option_d = models.CharField(max_length=200, blank=True, null=True)
    correct_option = models.CharField(max_length=1, help_text="A, B, C, or D")

    def __str__(self):
        return self.text[:50]
