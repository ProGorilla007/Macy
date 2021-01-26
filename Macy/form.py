from .models import User
from .models import Links
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


class UserForm(UserCreationForm):
    """新規登録フォーム"""

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields.pop('password1')
        # self.fields.pop('password2')
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs['autofocus'] = True


class LoginForm(AuthenticationForm):
    """ログインフォーム"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            # field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = field.label
