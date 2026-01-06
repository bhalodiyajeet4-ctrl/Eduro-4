from django.urls import path
from .views import AdminLoginView, TeacherLoginView, StudentLoginView

urlpatterns = [
    path('admin/login', AdminLoginView.as_view(), name='admin-login'),
    path('teacher/login', TeacherLoginView.as_view(), name='teacher-login'),
    path('student/login', StudentLoginView.as_view(), name='student-login'),
]
