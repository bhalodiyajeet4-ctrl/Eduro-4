from rest_framework import serializers
from .models import AdminUser, Teacher, Student


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdminUser
        fields = ['id', 'email', 'full_name', 'phone', 'is_active']


class TeacherSerializer(serializers.ModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)

    class Meta:
        model = Teacher
        fields = ['id', 'email', 'full_name', 'phone', 'employee_id', 'department', 'department_name', 'is_active']


class StudentSerializer(serializers.ModelSerializer):
    semester_info = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ['id', 'email', 'full_name', 'phone', 'roll_number', 'semester', 'semester_info', 'enrollment_year', 'is_active']

    def get_semester_info(self, obj):
        if obj.semester:
            return f"Semester {obj.semester.semester_number} - {obj.semester.course.name}"
        return None
