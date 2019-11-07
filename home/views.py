from django.contrib.auth.models import User
from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import EmailMessage

# Create your views here.
from home.form import SignUpForm, SignInForm, FeedBack


def homepage(request):
    return render(request , 'main.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        password_error = form.data.get('password1') != form.data.get('password2')
        username_error = User.objects.filter(username=form.data.get('username'))
        if password_error or username_error:
            return render(request, 'signup.html', {'form': SignUpForm(), 'password_error': password_error,
                                                   'username_error': username_error})
        if form.is_valid():
            user = form.save(commit=False)
            user.created_by = request.user
            user.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):
    error = False
    if request.method == 'POST':
        form = SignInForm(request.POST)
        form.is_valid()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password')
        user = authenticate(username=username, password=raw_password)
        if user:
            login(request, user)
            return redirect('/')
        else:
            error = True
    else:
        form = SignInForm()
    return render(request, 'signin.html', {'form': form, 'error': error})


def contact_us(request):
    if request.method == 'POST':
        form = FeedBack(request.POST)
        form.is_valid()
        email = EmailMessage(form.cleaned_data.get('title'), form.cleaned_data.get('text') + form.cleaned_data.get(
            'email'), to=[form.cleaned_data.get('email')])
        email.send()
        return render(request, 'success.html')
    else:
        form = FeedBack()
    return render(request, 'feedback.html', {'form': form})


def success(request):
    return render(request, 'success.html')
