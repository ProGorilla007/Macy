from django.views.generic import TemplateView, ListView,DeleteView
from django.views.generic.edit import FormView, CreateView
from Macy.form import UserForm
from django.urls import reverse_lazy
from .models import User


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('account')


class AccountView(TemplateView):
    template_name = "registration/account.html"


class UserList(ListView):
    model = User
    template_name = "User_list.html"


class MemberDelete(DeleteView):
    model = User
    success_url = reverse_lazy("user")

