from django.urls import path
from .views import register, login_view, logout_view, dashboard, add_course, enroll_course, view_course, landing_page, teacher, courses

urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('dashboard/', dashboard, name='dashboard'),
    path('teacher/', teacher, name='teacher'),
    path('courses/', courses, name='courses'),
    path('add_course/', add_course, name='add_course'),
    path('enroll/<int:course_id>/', enroll_course, name='enroll_course'),
    path('course/<int:course_id>/', view_course, name='view_course'),
]
