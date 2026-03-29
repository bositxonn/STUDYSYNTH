from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib import messages
from .models import Course, Lesson, Quiz, Category

class CatalogView(ListView):
    model = Course
    template_name = 'index.html'
    context_object_name = 'courses'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class CourseDetailView(DetailView):
    model = Course
    template_name = 'courses/detail.html'
    context_object_name = 'course'

class LessonView(LoginRequiredMixin, DetailView):
    model = Lesson
    template_name = 'courses/lesson.html'
    context_object_name = 'lesson'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.subscriptions.filter(is_active=True).exists():
            messages.error(request, "A premium subscription is required to access learning materials.")
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

class QuizView(LoginRequiredMixin, DetailView):
    model = Quiz
    template_name = 'courses/quiz.html'
    context_object_name = 'quiz'

    def post(self, request, *args, **kwargs):
        quiz = self.get_object()
        correct = 0
        total = quiz.questions.count()
        if total == 0:
            messages.error(request, "This quiz currently has no questions to score.")
            return redirect('lesson-detail', pk=quiz.lesson.id)
            
        for q in quiz.questions.all():
            answer = request.POST.get(f'q_{q.id}')
            if answer == q.correct_option:
                correct += 1
        
        score = (correct / total) * 100
        if score >= quiz.passing_score:
            messages.success(request, f"Outstanding! You passed with {score:.0f}%. Your profile has been updated.")
            # Optionally: update profile models here!
        else:
            messages.error(request, f"You scored {score:.0f}%, which is below the {quiz.passing_score}% requirement. Please review the lesson and try again!")
            
        return redirect('lesson-detail', pk=quiz.lesson.id)
