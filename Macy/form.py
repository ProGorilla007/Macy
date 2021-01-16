from django import forms
from .models import User
from .models import Links


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name', 'password')
