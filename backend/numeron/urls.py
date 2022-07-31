from django.urls import path
from . import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
    path('login/', views.login, name='login'),
    path('new/', views.new, name='new'),
    path('index/', views.index, name='index'),
    path('detail/', views.detail, name='detail'),
    path('ranking/', views.ranking, name='ranking'),
    path('setting/', views.setting, name='setting'),
    path('getRanking/', views.getRanking, name='getRanking'),
]