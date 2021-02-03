from .models import User
from django.forms import ModelForm, inlineformset_factory
from .models import Links
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordResetForm, SetPasswordForm
from django import forms


class UserForm(UserCreationForm):
    """新規登録フォーム"""

    class Meta:
        model = User

        fields = ('username', 'first_name', 'last_name', 'intro', 'email')
        labels = {
            'username': 'ユーザー名',
            'first_name': '名前',
            'last_name': '氏名',
            'intro': '自己紹介',
        }
        widgets = {
            'intro': forms.Textarea(attrs={'placeholder': '簡単な自己紹介を書いてね！'}),
        }


    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password1')
        # self.fields.pop('password2')
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


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


UserSignupFormSet = inlineformset_factory(User, Links, form=LinksForm, exclude=("id",), extra=3, can_delete=False)


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
