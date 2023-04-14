from django.urls import path
from . import views

urlpatterns = [
    path('backend/', views.backend, name='backend'),
    #path('result/', views.result, name='result'),
    path('quiz/', views.quiz, name='quiz'),
    #path('reset/', views.reset_answers, name='reset_answers'),
]