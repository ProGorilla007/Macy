import base64
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, DetailView, DeleteView
from django.views.generic.edit import CreateView, UpdateView
from Macy.forms import UserForm, LoginForm, UserEditForm, UserEditFormSet, \
    MyPasswordResetForm, MySetPasswordForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import get_user_model, login
from django.shortcuts import redirect, get_object_or_404
import qrcode
from io import BytesIO


User = get_user_model()


class IndexView(TemplateView):
    template_name = "index.html"


class MypageView(DetailView):
    template_name = "mypage.html"
    model = User

    @staticmethod
    def make_qr(request):
        qr_img = qrcode.make(request.build_absolute_uri())
        buffer = BytesIO()
        qr_img.save(buffer, format="PNG")
        img = base64.b64encode(buffer.getvalue()).decode().replace("'", "")
        request.qr = img

    def get(self, request, *args, **kwargs):
        user = User.objects.get(user_id=kwargs['id'])
        if user.is_direct:
            return HttpResponseRedirect(user.direct_link)

        self.make_qr(request)

        return super().get(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return User.objects.get(user_id=self.kwargs.get("id"))


class SignupView(SuccessMessageMixin, CreateView):
    form_class = UserForm
    template_name = "registration/signup.html"
    success_message = "ユーザ認証が完了しました。以下よりアカウント情報の追加/編集を行ってください。"

    def get(self, request, *args, **kwargs):
        self.object = None
        # プロダクトコードがアクティベイトされていたら、Indexにリダイレクトする
        if User.objects.get(user_id=self.kwargs.get("id")).is_active:
            return redirect('/')
        # 空のフォームをレンダーする
        form = self.get_form(self.form_class)
        return self.render_to_response(
            self.get_context_data(form=form))

    def get_success_url(self):
        # Postが成功したらユーザーをログインして編集画面に転移する
        login(self.request, self.object)
        messages.add_message(self.request, messages.INFO, self.success_message)
        return reverse_lazy('edit', kwargs={'id': self.object.user_id})

    def post(self, request, *args, **kwargs):
        self.object = None
        user_update = get_object_or_404(User, user_id=self.kwargs.get("id"))
        form = UserForm(self.request.POST, request.FILES, instance=user_update)
        if form.is_valid():
            user_update.is_active = True
            user_update.save()
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(
            self.get_context_data(form=form))


class AccountView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = "registration/account.html"
    model = User

    def test_func(self):
        # idが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser

    def get_object(self, queryset=None):
        return User.objects.get(user_id=self.kwargs.get("id"))


class UserEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = "registration/edit.html"
    model = User
    form_class = UserEditForm

    def get_form_kwargs(self):
        kwargs = super(UserEditView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'id': self.request.user.user_id})
        return url

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser

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
        initial['intro'] = self.request.user.intro
        return initial

    def post(self, request, *args, **kwargs):
        self.object = None
        user_update = get_object_or_404(User, user_id=self.request.user.user_id)

        formset = UserEditFormSet(self.request.POST)

        # create instance for each link forms
        i = 0  # counter
        for instance in self.request.user.links_set.all():
            link_form = formset.forms[i]
            link_form.instance = instance
            i += 1

        form = UserEditForm(self.request.POST, self.request.FILES, instance=user_update, request=self.request)

        # if both user form and link forms are valid, pass those forms to form_valid and save the changes
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset):

        # save user info such as usernames and emails.
        self.object = form.save()

        if form.cleaned_data['direct_link'] is not None:
            self.request.user.set_direct_link(form.cleaned_data['direct_link'])

        # overwrite the formset info with new input.
        formset.instance = self.object

        # delete objects in deleted forms.
        for obj in formset.deleted_forms:
            if obj.instance.id is not None:
                obj.instance.delete()

        # save objects in formset excluding deleted forms.
        formset.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, links_form):
        return self.render_to_response(
            self.get_context_data(form=form,
                                  links_form=links_form))


class UserDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    template_name = "registration/user_delete_confirm.html"
    model = User
    success_url = reverse_lazy("index")
    success_message = "ユーザー削除が完了しました"

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser


class DeleteProfileView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'registration/blank.html'

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'id': self.request.user.user_id})
        return url

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.profile.delete()
        return HttpResponseRedirect(success_url)


class DeleteHeaderView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'registration/blank.html'

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'id': self.request.user.user_id})
        return url

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.header.delete()
        return HttpResponseRedirect(success_url)


class IsDirectView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    model = User
    template_name = 'registration/blank.html'

    def test_func(self):
        # pkが現在ログイン中ユーザと同じ、またはsuperuserならOK。
        current_user = self.request.user
        return current_user.user_id == self.kwargs['id'] or current_user.is_superuser

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'id': self.request.user.user_id})
        return url

    def get(self, request, *args, **kwargs):
        self.object = User.objects.get(user_id=self.request.user.user_id)
        self.object.toggle_direct()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    template_name = "registration/password_change.html"

    def get_success_url(self):
        return reverse('password_change_done', kwargs={'id': self.request.user.user_id})


class UserPasswordChangeDoneView(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = "registration/password_change_done.html"


class UserPasswordResetView(PasswordResetView):
    """パスワード変更用URLの送付ページ"""
    subject_template_name = 'registration/mail_template/create/subject.txt'
    email_template_name = 'registration/mail_template/create/message.txt'
    template_name = 'registration/password_reset_form.html'
    form_class = MyPasswordResetForm
    success_url = reverse_lazy('password_reset_done')


class UserPasswordResetDoneView(PasswordResetDoneView):
    """パスワード変更用URLを送りましたページ"""
    template_name = 'registration/password_reset_done.html'


class UserPasswordResetConfirmView(PasswordResetConfirmView):
    """新パスワード入力ページ"""
    form_class = MySetPasswordForm
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'registration/password_reset_confirm.html'

    def get_success_url(self):

        return reverse('password_reset_complete')


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """新パスワード設定しましたページ"""
    template_name = 'registration/password_reset_complete.html'


class LogInView(LoginView):
    form_class = LoginForm
    template_name = "registration/login.html"

    def get_success_url(self):
        url = reverse_lazy('users', kwargs={'id': self.request.user.user_id})
        return url


class LogOutView(LogoutView):
    pass


class AboutView(TemplateView):
    template_name = "about.html"


class GuideView(TemplateView):
    template_name = "guide.html"


class ContactView(TemplateView):
    template_name = "contact.html"
