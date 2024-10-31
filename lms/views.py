from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm, CourseForm
from .models import Course, Enrollment, UserProfile
from django.contrib.auth.models import User



def landing_page(request):
    user_profile = None
    if request.user.is_authenticated:
        user_profile = UserProfile.objects.get(user=request.user)
    return render(request, 'landing_page.html', {'user_profile': user_profile})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            user_profile = UserProfile(user=user, user_type=form.cleaned_data['user_type'])
            user_profile.save()
            
            login(request, user)
            
            # Redirect based on user type
            if user_profile.is_teacher():
                return redirect('teacher')  
            else:
                return redirect('dashboard')  
    else:
        form = RegistrationForm()
    
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')  
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('landing_page')

@login_required
def dashboard(request):
    user_profile = request.user.userprofile

    if user_profile.is_student():
        
        enrolled_courses = Enrollment.objects.filter(student=user_profile)
       
        available_courses = Course.objects.exclude(enrollment__student=user_profile)
        
        all_teachers = UserProfile.objects.filter(user_type='teacher')
        
        context = {
            'enrolled_courses': enrolled_courses,
            'available_courses': available_courses,
            'user_profile': user_profile,  
            'all_teachers': all_teachers,  
        }
    elif user_profile.is_teacher():
        
        created_courses = Course.objects.filter(created_by=user_profile)
        available_courses = Course.objects.exclude(enrollment__student=user_profile)
        context = {
            'created_courses': created_courses,
            'user_profile': user_profile,
        }
    
    return render(request, 'dashboard.html', context)

@login_required
def teacher(request):
    
    user_profile = request.user.userprofile

    if user_profile.is_teacher():
        
        all_teachers = UserProfile.objects.filter(user_type='teacher')

        created_courses = Course.objects.filter(created_by=user_profile)

        
        context = {
            'created_courses': created_courses,  
            'user_profile': user_profile,        
            'all_teachers': all_teachers,               
        }

        return render(request, 'teacher.html', context)
    else:
        all_teachers = UserProfile.objects.filter(user_type='teacher')
        
        
        all_students = UserProfile.objects.filter(user_type='student')

        created_courses = Course.objects.filter(created_by=user_profile)

        
        context = {
            'created_courses': created_courses,  
            'user_profile': user_profile,        
            'all_teachers': all_teachers,               
        }
        return render(request, 'student_teachers.html', context)

@login_required
def courses(request):
    user_profile = request.user.userprofile

    available_courses = Course.objects.exclude(enrollment__student=user_profile)

    created_courses = Course.objects.filter(created_by=user_profile)

    context = {
            'created_courses': created_courses,
            'user_profile': user_profile,
            'available_courses': available_courses
        }

    return render(request, 'courses.html',context)


@login_required
def enroll_course(request, course_id):
    user_profile = request.user.userprofile
    course = get_object_or_404(Course, id=course_id)

    if user_profile.is_student():
        Enrollment.objects.get_or_create(student=user_profile, course=course)
        return redirect('dashboard')
    else:
        return redirect('dashboard')  


@login_required
def view_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    context = {
        'course': course
    }
    return render(request, 'view_course.html', context)

@login_required
def add_course(request):
    user_profile = request.user.userprofile

    if user_profile.is_teacher():
        if request.method == 'POST':
            form = CourseForm(request.POST)
            if form.is_valid():
                course = form.save(commit=False)
                course.created_by = user_profile
                course.save()
                return redirect('dashboard')
        else:
            form = CourseForm()
        return render(request, 'add_course.html', {'form': form})
    else:
        return redirect('dashboard')
