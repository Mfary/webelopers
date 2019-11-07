from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form


class SignUpForm(UserCreationForm):
    user_name = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(
        label="password",
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="password confirm",
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class SignInForm(Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ('username', 'password1', )
