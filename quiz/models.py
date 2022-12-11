import random

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from random import shuffle

a = 0


def validate_correct_check(question_id):
    global a
    print(a)
    if (Answer.objects.filter(question_id=question_id).count()
        - Answer.objects.filter(question_id=question_id, correct__in=[True]).count() == 1) \
            and a == 1:
        print('124', a)
        a = 0
        raise ValidationError('124')

    elif (Answer.objects.filter(question_id=question_id).count()
          - Answer.objects.filter(question_id=question_id, correct__in=[False]).count() == 1) \
            and a == -1:
        print('123', a)
        a = 0
        raise ValidationError('123')
    return question_id


def validate_correct_checkin(correct):
    global a
    if correct is False:
        a -= 1
    elif correct is True:
        a += 1
    return correct


class Category(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование категории')

    def get_absolute_url(self):
        return reverse('category',
                       kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['title']


class Quiz(models.Model):
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, max_length=120,
                                 verbose_name='Категория')
    topic = models.CharField(max_length=120, verbose_name='Тема')
    description = models.TextField(blank=True, verbose_name='Описание')
    number_of_questions = models.IntegerField(verbose_name='Количество вопросов')

    def __str__(self):
        return f"{self.category}-{self.topic}"

    def get_absolute_url(self):
        return reverse('view_quiz',
                       kwargs={'pk': self.pk})

    def get_questions(self):
        question = list(self.question_set.all())
        random.shuffle(question)
        return question[:self.number_of_questions]

    class Meta:
        verbose_name = 'Тест'
        verbose_name_plural = 'Тесты'


class Question(models.Model):
    text = models.CharField(max_length=200, verbose_name='Текст вопроса')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Тест')
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return str(self.text)

    def get_answers(self):
        return self.answer_set.all()

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    text = models.CharField(max_length=200, verbose_name='Текст ответа')
    correct = models.BooleanField(default=False, verbose_name='Правильно',
                                  validators=[validate_correct_checkin])
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='Вопрос',
                                 validators=[validate_correct_check])
    created = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    def __str__(self):
        return f"вопрос: {self.question.text}, ответ: {self.text}, правильно: {self.correct}"

    def save(
            self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        global a
        a = 0
        super().save()

    def clean(self):
        global a
        if abs(a) == Answer.objects.filter(question_id=self.question_id).count():
            a = 0
            raise ValidationError('vev')

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'


class Result(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, verbose_name='Тест')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    score = models.FloatField(verbose_name='Очки')

    def __str__(self):
        return str(self.pk)

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'
