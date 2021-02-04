from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from Macy.form import UserForm, LoginForm, UserSignupFormSet, UserEditForm, UserEditFormSet, MyPasswordResetForm, MySetPasswordForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, get_object_or_404


User = get_user_model()


class IndexView(TemplateView):
    template_name = "index.html"


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_message = "ユーザ登録が完了しました。以下よりアカウントの情報が確認できます。"

    def get(self, request, *args, **kwargs):
        self.object = None
        if self.request.user.is_authenticated:
            return redirect('/')
        form = self.get_form(self.form_class)
        links_form = UserSignupFormSet()
        return self.render_to_response(
            self.get_context_data(form=form,
                                  links_form=links_form))

    def get_success_url(self):
        login(self.request, self.object)
        return reverse_lazy('users', kwargs={'slug': self.object.slug})

    def post(self, request, *args, **kwargs):
        formset = UserSignupFormSet(self.request.POST)
        form = self.get_form()
        if form.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class AccountView(UserPassesTestMixin, LoginRequiredMixin, DetailView):
    permission_denied_message = "お手数ですがログイン後、もう一度お試しください"
    template_name = "registration/account.html"
    model = User

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.slug == self.kwargs['slug'] or current_user.is_superuser


class UserEditView(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    template_name = "registration/edit.html"
    model = User
    form_class = UserEditForm
    success_url = reverse_lazy("index")

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.slug == self.kwargs['slug'] or current_user.is_superuser

    def get(self, request, *args, **kwargs):
        self.object = None
        form = self.get_form(self.form_class)
        links_form = UserEditFormSet(
            initial=[{'media_choice': link.media_choice,
                      'link': link.link,
                      'account_id': link.account_id,
                      } for link in self.request.user.links_set.all()]
        )
        return self.render_to_response(
            self.get_context_data(form=form,
                                  links_form=links_form))

    def get_initial(self):
        initial = super().get_initial()
        initial['username'] = self.request.user.username
        initial['email'] = self.request.user.email
        initial['first_name'] = self.request.user.first_name
        initial['last_name'] = self.request.user.last_name
        initial['intro'] = self.request.user.intro

        return initial

    def post(self, request, *args, **kwargs):

        user_update = get_object_or_404(User, slug=self.request.user.slug)

        formset = UserEditFormSet(self.request.POST)

        # create instance for each link forms
        i = 0  # counter
        for instance in self.request.user.links_set.all():
            link_form = formset.forms[i]
            link_form.instance = instance
            i += 1

        form = UserEditForm(self.request.POST, instance=user_update)

        # if both user form and link forms are valid, pass those forms to form_valid and save the changes
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):

        self.object = form.save()
        formset.instance = self.object
        links = formset.save()

        # assign each data to link instance and save the changes
        i = 0  # counter
        for link in links:
            link.media_choice = formset.cleaned_data[i]['media_choice']
            link.link = formset.cleaned_data[i]['link']
            link.account_id = formset.cleaned_data[i]['account_id']
            link.save()
            i += 1

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, links_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  links_form=links_form))


class MypageView(DetailView):
    template_name = "mypage.html"
    model = User


class UserDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    template_name = "registration/user_delete_confirm.html"
    model = User
    success_url = reverse_lazy("index")
    success_message = "ユーザー削除が完了しました"

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.slug == self.kwargs['slug'] or current_user.is_superuser


class LogInView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'slug': self.request.user.slug})
        return url


class AboutView(TemplateView):
    template_name = "about.html"


class GuideView(TemplateView):
    template_name = "guide.html"


class ContactView(TemplateView):
    template_name = "contact.html"


class PasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change.html"

    def get_success_url(self):
        return reverse('password_change_done', kwargs={'slug': self.user.slug})


class PasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class PasswordResetView(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'registration/mail_template/create/subject.txt'
    email_template_name = 'registration/mail_template/create/message.txt'
    template_name = 'registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class PasswordResetDoneView(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'


class PasswordResetConfirmView(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

    def get_success_url(self):

        return reverse('password_reset_complete')


class PasswordResetCompleteView(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'
