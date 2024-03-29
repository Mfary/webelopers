from itertools import chain

from django.contrib.auth.decorators import login_required
from django.db.models import QuerySet
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

# Create your views here.
from django.views import static

from home.form import SignUpForm, SignInForm, FeedBack, ProfileForm, MakeCourseForm
from home.models import Course, Profile


def homepage(request):
    return render(request, 'main.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        password_error = form.data.get('password1') != form.data.get('password2')
        username_error = Profile.objects.filter(username=form.data.get('username'))
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
        # email = EmailMessage(subject=form.cleaned_data.get('title'), body=form.cleaned_data.get('email') + '\n' + form.
        #                      cleaned_data.get('text') + '\n', to=['webe19lopers@gmail.com'])
        # email.send()
        return render(request, 'success.html')
    else:
        form = FeedBack()
    return render(request, 'feedback.html', {'form': form})


def success(request):
    return render(request, 'success.html')


@login_required(login_url='/login')
def profile(request):
    image = Profile.objects.get(username=request.user.username).image
    print(request.user.username)
    return render(request, 'profile.html', {'firstname': request.user.first_name, 'lastname': request.user.last_name,
                                            'username': request.user.username, 'image': image.url if image else "s"})


@login_required(login_url='/login')
def change(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        user_profile = Profile.objects.get(username=request.user.username)
        if form.data.get('first_name'):
            user_profile.first_name = form.data.get('first_name')
            user_profile.save()
        if form.data.get('last_name'):
            user_profile.last_name = form.data.get('last_name')
            user_profile.save()
        if len(request.FILES):
            user_profile.image = request.FILES.get('image')
            user_profile.save()
        return redirect('/profile')
    return render(request, 'change.html', {'form': ProfileForm()})


@login_required(login_url='/login')
def panel(request):
    return render(request, 'panel.html')


@login_required(login_url='/login')
def make_course(request):
    if request.method == 'POST':
        form = MakeCourseForm(request.POST)
        course = form.save(commit=False)
        # save course
        course.save()
        return redirect('/')
    else:
        form = MakeCourseForm()
    return render(request, 'makecourse.html', {'form': form})


@login_required(login_url='/login')
def show_courses(request):
    courses = Course.objects.all()
    search_courses = QuerySet().none()
    if request.POST:
        search = True
        if not request.POST.get('department') and not request.POST.get('teacher') and not request.POST.get('course'):
            search_courses = search_courses | Course.objects.filter(department=request.POST.get('search_query'))
        if request.POST.get('department'):
            search_courses = search_courses | Course.objects.filter(department=request.POST.get('search_query'))
        if request.POST.get('teacher'):
            search_courses = search_courses | Course.objects.filter(teacher=request.POST.get('search_query'))
        if request.POST.get('course'):
            search_courses = search_courses | Course.objects.filter(name=request.POST.get('search_query'))
    else:
        search = False
    username_courses = Profile.objects.get(username=request.user.username).courses
    return render(request, 'courses.html', {'courses': courses, 'search': search, 'search_courses': search_courses,
                                            'my_courses': username_courses.all() if username_courses else None})


@login_required(login_url='/login')
def register_course(request, course_id):
    course = Course.objects.get(course_number=course_id)
    profile = Profile.objects.get(username=request.user.username)
    profile.courses.add(course)
    return redirect('/courses')


@login_required(login_url='/login')
def remove_course(request , course_id):
    course = Course.objects.get(course_number=course_id)
    course.num -= 1
    profile = Profile.objects.get(username=request.user.username)
    profile.courses.remove(course)
    return redirect('/courses')


@login_required(login_url='/login')
def course_detail(request , course_id):
    course = Course.objects.get(course_number=course_id)
    course.num +=1
    return render(request, 'detail.html', {'course': course})
