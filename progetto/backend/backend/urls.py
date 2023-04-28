from django.urls import path
from . import views

urlpatterns = [
    path('backend/', views.backend, name='backend'),
    #path('result/', views.result, name='result'),
    path('quiz/', views.quiz, name='quiz'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    #path('reset/', views.reset_answers, name='reset_answers'),
]