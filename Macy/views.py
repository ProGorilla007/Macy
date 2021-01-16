from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(TemplateView):
    template_name = "registration/signup.html"


class AccountView(TemplateView):
    template_name = "registration/account.html"
