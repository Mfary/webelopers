from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import Form, ModelForm

from home.models import Course, Profile


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=20, required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(max_length=254, required=True)
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = Profile
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class SignInForm(Form):
    username = forms.CharField(max_length=30, required=True)
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput)

    class Meta:
        model = Profile
        fields = ('username', 'password1', )


class FeedBack(Form):
    title = forms.CharField(max_length=30, required=True)
    email = forms.EmailField(required=True)
    text = forms.CharField(min_length=10, max_length=250 , required=True , widget=forms.Textarea)


class ProfileForm(Form):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    image = forms.ImageField(required=False)

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'image')


class MakeCourseForm(ModelForm):
    choice = {('0', 'Saturday'), ('1', 'Sunday'), ('2', 'Monday'), ('3', 'Tuesday'), ('4', 'Wednesday')}
    department = forms.CharField(max_length=50 , required=True)
    name = forms.CharField(max_length=50, required=True)
    course_number = forms.IntegerField(required=True)
    group_number = forms.IntegerField(required=True)
    teacher = forms.CharField(max_length=60, required=True)
    start_time = forms.TimeField(required=True)
    end_time = forms.TimeField(required=True)
    first_day = forms.ChoiceField(choices=choice, required=True)
    second_day = forms.ChoiceField(choices=choice, required=False)
    exam_date = forms.DateField()

    class Meta:
        model = Course
        fields = {'department', 'name', 'course_number', 'group_number', 'teacher', 'start_time', 'end_time',
                  'first_day', 'second_day', 'exam_date'}
