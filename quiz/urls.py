from django.urls import path

from .views import HomeQuiz, RegisterFormView, LoginFormView, user_logout, QuizByCategory, quiz_data_view, ViewQuiz, \
    quiz_save_view

urlpatterns = [
    path('', HomeQuiz.as_view(), name='home'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', user_logout, name='logout'),
    path('category/<int:category_id>/', QuizByCategory.as_view(), name='category'),
    path('quiz/<int:pk>/', ViewQuiz.as_view(), name='view_quiz'),
    path('quiz/<int:pk>/data', quiz_data_view, name='quiz_data_view'),
    path('quiz/<int:pk>/save', quiz_save_view, name='quiz_save_view'),
]
