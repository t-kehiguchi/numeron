from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('new/', views.new, name='new'),
    path('getRanking/', views.getRanking, name='getRanking'),
    path('hello/', views.hello, name='hello'),
]