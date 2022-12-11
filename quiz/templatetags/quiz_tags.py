from django import template
from django.db.models import Count

from quiz.models import Category

register = template.Library()


@register.simple_tag
def get_quizzes():
    return Category.objects.all()


@register.inclusion_tag('quiz/list_quiz_topic.html')
def show_quizzes():
    quizzes = Category.objects.annotate(cnt=Count('quiz')).filter(cnt__gt=0)
    return {'quizzes': quizzes}

