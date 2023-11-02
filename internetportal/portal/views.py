from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import TemplateView

from .forms import *
from .models import *


class Index(generic.ListView):
    model = Application
    template_name = 'index.html'
    context_object_name = 'applications'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["num_of_accepted_apps"] = Application.objects.filter(status__exact='a').count()
        return context

    def get_queryset(self):
        return Application.objects.filter(status__exact='d').order_by('-date')[:4]


class RegisterUserView(generic.CreateView):
    model = AdvUser
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')


class LoginUserView(views.LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')


class LogoutUserView(LoginRequiredMixin, views.LogoutView):
    template_name = 'registration/logout.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'personal/user_personal.html'
