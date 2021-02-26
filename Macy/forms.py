from django.core.exceptions import ValidationError

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

        fields = ('email',)
        labels = {
            'email': 'メールアドレス',
        }
        help_texts = {
        }

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password1')
        # self.fields.pop('password2')
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


class UserEditForm(UserChangeForm):
    direct_link = forms.ModelChoiceField(queryset=None, required=False)

    class Meta:
        model = User
        fields = ('username', 'profile', 'header', 'intro')
        labels = {
            'username': '名前',
            'profile': 'プロフィール画像',
            'header': 'ヘッダー画像',
            'intro': '自己紹介',
        }
        help_texts = {
            # 'username': 'ユーザーネームの再設定はできません。',
            'profile': '1500px*1500px未満、2MB以下の画像がお使いいただけます。',
            'header': '2000px*2000px未満、2MB以下の画像がお使いいただけます。',
        }

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(UserEditForm, self).__init__(*args, **kwargs)
        # self.fields['username'].disabled = True
        self.fields['direct_link'].queryset = Links.objects.filter(user_id=self.request.user.user_id)
        self.fields.pop('password')

    def clean_profile(self):
        profile = self.cleaned_data['profile']
        if profile is not None:
            profile_width = 1500
            if profile.image.width > profile_width:
                raise ValidationError(
                    'この画像の幅は%spxです。%spx以下の横幅の画像の登録をお願いします' % (profile.image.width, profile_width)
                )

            profile_height = 1500
            if profile.image.height > profile_height:
                raise ValidationError(
                    'この画像の高さは%spxです。%spx以下の縦幅の画像の登録をお願いします' % (profile.image.width, profile_height)
                )

            img_size = 2*1000*1000
            if profile.size > img_size:
                raise ValidationError(
                    '画像が大きすぎます。%sMBより小さいサイズの画像をお願いします。' % str(img_size//1000//1000)
                )

    def clean_header(self):
        header = self.cleaned_data['header']
        if header is not None:
            img_width = 2000
            if header.image.width > img_width:
                raise ValidationError(
                    'この画像の幅は%spxです。%spx以下の横幅の画像の登録をお願いします' % (header.image.width, img_width)
                )

            img_height = 2000
            if header.image.height > img_height:
                raise ValidationError(
                    'この画像の高さは%spxです。%spx以下の縦幅の画像の登録をお願いします' % (header.image.width, img_height)
                )

            img_size = 2 * 1000 * 1000
            if header.size > img_size:
                raise ValidationError(
                    '画像が大きすぎます。%sMBより小さいサイズの画像をお願いします。' % str(img_size // 1000 // 1000)
                )


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
        self.fields['media_choice'].widget.attrs['class'] = 'link-choice'
        self.fields['link'].widget.attrs['class'] = 'link-url'
        self.fields['link'].widget.attrs['readonly'] = True
        self.fields['account_id'].widget.attrs['class'] = 'link-account'


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
