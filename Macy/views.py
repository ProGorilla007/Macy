from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import FormView, CreateView
from Macy.form import UserForm, LoginForm
from django.urls import reverse_lazy
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('login_view')
    success_message = "ユーザ登録が完了しました。以下フォームよりログインください。"


class AccountView(LoginRequiredMixin, DetailView):
    permission_denied_message = "お手数ですがログイン後、もう一度お試しください"
    template_name = "registration/account.html"
    model = User


class UserList(ListView):
    model = User
    template_name = "User_list.html"


class LogInView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"
