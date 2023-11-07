from django.contrib import messages
from django.contrib.auth import views
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import generic

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
    template_name = 'registration/register.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('index')


class LoginUserView(views.LoginView):
    template_name = 'registration/login.html'
    success_url = reverse_lazy('index')


class LogoutUserView(LoginRequiredMixin, views.LogoutView):
    template_name = 'registration/logout.html'


class UserProfileView(LoginRequiredMixin, generic.ListView):
    template_name = 'personal/user_personal.html'
    model = Application
    context_object_name = 'apps'

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = Application.objects.filter(author=self.request.user).order_by('-date')
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class ApplicationCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'personal/create_application.html'
    model = Application
    form_class = ApplicationCreateForm
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ApplicationDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'personal/delete_application.html'
    model = Application
    success_url = reverse_lazy('profile')

    def get(self, request, *args, **kwargs):
        self.application = self.get_object()

        if self.application.status in ['a', 'd']:
            return HttpResponseRedirect(self.success_url)

        return super().get(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        self.application = self.get_object()

        if self.object.status in ['a', 'd']:
            return HttpResponseRedirect(self.success_url)

        return super().delete(request, *args, **kwargs)


class AdminView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'is_staff'
    template_name = 'personal/admin.html'
    model = Application
    context_object_name = 'applications'

    def get_queryset(self):
        status = self.request.GET.get('status')
        queryset = Application.objects.filter().order_by('-date')
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        return context


class AdminUpdateApplicationView(PermissionRequiredMixin, generic.UpdateView):
    permission_required = 'is_staff'
    template_name = 'personal/update_application.html'
    model = Application
    form_class = ApplicationUpdateStatusForm
    success_url = reverse_lazy('admin')


class AdminDeleteCategoryView(PermissionRequiredMixin, generic.DeleteView):
    permission_required = 'is_staff'
    template_name = 'personal/delete_category.html'
    model = Category
    success_url = reverse_lazy('admin')


class AdminCreateCategoryView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'is_staff'
    template_name = 'personal/create_category.html'
    model = Category
    form_class = CategoryCreateForm
    success_url = reverse_lazy('admin')
