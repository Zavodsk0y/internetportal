from django.urls import path
from .views import *
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', RegisterUserView.as_view(), name='registration'),
    path('login/', LoginUserView.as_view(), name='login'),
]