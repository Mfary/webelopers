from django.forms import Form
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.core.mail import send_mail

# Create your views here.
from home.form import SignUpForm, SignInForm, FeedBack


def homepage(request):
    return render(request , 'main.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.validate_unique()
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
        send_mail(
            form.cleaned_data.get('title'),
            form.cleaned_data.get('context') + form.cleaned_data.get('email'),
            'django@django.com',
            recipient_list=['clappleid@outlook.com'],
            auth_user='mohammadsadeghkeshavarzi@yahoo.com',
            auth_password='kSmS09193360118',
            fail_silently=False,
        )
        return redirect('/success')
    else:
        form = FeedBack()
    return render(request, 'feedback.html', {'form': form})


def success(request):
    return render(request, 'success.html')
