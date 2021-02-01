from django.views.generic import TemplateView, ListView, DetailView, DeleteView
from django.views.generic.edit import FormView, CreateView
from Macy.form import UserForm, LoginForm, MyPasswordResetForm, MySetPasswordForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login
from django.urls import reverse


User = get_user_model()


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_message = "ユーザ登録が完了しました。以下フォームよりログインください。"

    def get_success_url(self):
        login(self.request, self.object)
        return reverse('users', kwargs={'pk': self.object.id})


class AccountView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    permission_denied_message = "お手数ですがログイン後、もう一度お試しください"
    template_name = "registration/account.html"
    model = User

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.pk == self.kwargs['pk'] or current_user.is_superuser


class UserDelete(SuccessMessageMixin, DeleteView):
    template_name = "registration/user_delete_confirm.html"
    model = User
    success_url = reverse_lazy("index")
    success_message = "ユーザー削除が完了しました"


class LogInView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"


class AboutView(TemplateView):
    template_name = "about.html"


class GuideView(TemplateView):
    template_name = "guide.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change.html"
    success_url = reverse_lazy("password_change_done")


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"
    success_url = reverse_lazy("index")


class PasswordReset(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'registration/mail_template/create/subject.txt'
    email_template_name = 'registration/mail_template/create/message.txt'
    template_name = 'registration/password_reset_form.html'
    # form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDone(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    # form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

    def get_success_url(self):

        return reverse('password_reset_complete', kwargs={'pk': self.user.id})


class PasswordResetComplete(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'
    #success_url = reverse_lazy('index')
