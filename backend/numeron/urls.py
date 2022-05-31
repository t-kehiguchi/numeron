from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('login/', views.login, name='login'),
    path('new/', views.new, name='new'),
    path('index/', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('getRanking/', views.getRanking, name='getRanking'),
]