from django.contrib.auth import logout, login
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView

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
        questions = []
        data = request.POST
        data_ = dict(data.lists())
        data_.pop('csrfmiddlewaretoken')
        # print(data)
        print(data_)

        for k in data_.keys():
            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answers = None

        for q in questions:
            a_selected = request.POST.get(q.text)
            # print(a_selected)

            if a_selected != '':
                question_answers = Answer.objects.filter(question=q)
                # print(question_answers)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answers = a.text
                    else:
                        if a.correct:
                            correct_answers = a.text

                results.append({str(q): {'correct_answers': correct_answers, 'answered': a_selected}})
            else:
                results.append({str(q): 'not answered'})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

    return JsonResponse({'score': score_, 'results': results})



