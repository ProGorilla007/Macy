from .models import User
from django.forms import ModelForm, inlineformset_factory
from .models import Links
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, \
    UserChangeForm, PasswordResetForm, SetPasswordForm
from django import forms


class UserForm(UserCreationForm):
    """新規登録フォーム"""

    class Meta:
        model = User

        fields = ('username', 'email', 'first_name', 'last_name', 'intro', 'email')
        labels = {
            'username': 'ユーザー名',
            'email': 'メールアドレス',
            'first_name': '名前',
            'last_name': '氏名',
            'intro': '自己紹介',
        }
        widgets = {
            'intro': forms.Textarea(attrs={'placeholder': '簡単な自己紹介を書いてね！'}),
        }
        help_texts = {
            'username': '150文字以内で入力してください。英数字と以下の記号がお使いいただけます。@/./+/-/_',
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password1')
        # self.fields.pop('password2')
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


class UserEditForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'intro')
        labels = {
            'username': '名前',
            'email': 'メールアドレス',
            'first_name': '名前',
            'last_name': '氏名',
            'intro': '自己紹介',
        }
        help_texts = {
            'username': 'ユーザーネームの再設定はできません。',
        }

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        self.fields['username'].disabled = True
        self.fields.pop('password')


class LinksForm(ModelForm):
    class Meta:
        model = Links
        fields = ('media_choice', 'link', 'account_id')
        labels = {
            'media_choice': 'SNS',
            'link': 'リンクURL',
            'account_id': 'ユーザーID',
        }
        widgets = {
            'link': forms.TextInput(attrs={'placeholder': '例）https://twitter.com/アカウント名'}),
            'account_id': forms.TextInput(attrs={'placeholder': '@twitter_official'}),
        }

    def __init__(self, *args, **kwargs):
        super(LinksForm, self).__init__(*args, **kwargs)


UserSignupFormSet = inlineformset_factory(User, Links, form=LinksForm, extra=4, can_delete=False)
UserEditFormSet = inlineformset_factory(
    User, Links, form=LinksForm, extra=10, can_delete=True)


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label


class MyPasswordResetForm(PasswordResetForm):
    """パスワード忘れたときのフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'


class MySetPasswordForm(SetPasswordForm):
    """パスワード再設定用フォーム(パスワード忘れて再設定)"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
