from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

from .logic import scored_logic
from .models import Quiz, Category, Question, Answer, Result
from .forms import UserRegisterFrom, UserLoginForm


class HomeQuiz(ListView):
    model = Quiz
    template_name = 'quiz/home_quiz.html'
    context_object_name = 'quiz'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return Quiz.objects.all().select_related('category')


class RegisterFormView(FormView):
    form_class = UserRegisterFrom

    template_name = 'quiz/register.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginFormView(LoginView):
    form_class = UserLoginForm

    template_name = 'quiz/login.html'

    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        return redirect('home')


def user_logout(request):
    logout(request)
    return redirect('login')


class QuizByCategory(ListView):
    model = Quiz
    template_name = 'quiz/home_quiz.html'
    context_object_name = 'quiz'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

    def get_queryset(self):
        return Quiz.objects.filter(id=self.kwargs['category_id']).select_related('category')


class ViewQuiz(DetailView):
    model = Quiz
    context_object_name = 'quiz_item'


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    question = []
    for q in quiz.get_questions():
        answers = []
        for a in q.get_answers():
            answers.append(a.text)
        question.append({str(q): answers})
    return JsonResponse({
        'data': question,
    })


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def quiz_save_view(request, pk):
    if is_ajax(request=request):
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        return scored_logic(data_, request, pk)
