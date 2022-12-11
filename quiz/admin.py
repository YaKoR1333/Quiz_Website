from django.contrib import admin
from .models import Question, Answer, Result, Quiz, Category


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerInline]


admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)
admin.site.register(Result)
admin.site.register(Quiz)
admin.site.register(Category)
