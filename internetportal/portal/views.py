from django.contrib.auth import views
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from .forms import *
from .models import *


class Index(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'applications'

    def get_queryset(self):
        return Application.objects.filter(status__exact='d').order_by('date')




class RegisterUserView(generic.CreateView):
    model = AdvUser
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')

class LoginUserView(views.LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')
