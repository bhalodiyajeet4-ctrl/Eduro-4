from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class AdminUser(models.Model):
    """Admin user model with separate authentication."""
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'admin_users'
        verbose_name = 'Admin User'
        verbose_name_plural = 'Admin Users'

    def __str__(self):
        return f"{self.full_name} ({self.email})"

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return check_password(raw_password, self.password)


class Teacher(models.Model):
    """Teacher user model with separate authentication."""
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True)
    department = models.ForeignKey('academic.Department', on_delete=models.SET_NULL, null=True, related_name='teachers')
    is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='teachers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teachers'
        verbose_name = 'Teacher'
        verbose_name_plural = 'Teachers'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['employee_id']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return check_password(raw_password, self.password)


class Student(models.Model):
    """Student user model with separate authentication."""
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20, blank=True, null=True)
    roll_number = models.CharField(max_length=50, unique=True)
    semester = models.ForeignKey('academic.Semester', on_delete=models.SET_NULL, null=True, related_name='students')
    enrollment_year = models.CharField(max_length=4)
    is_active = models.BooleanField(default=True)
    profile_photo = models.ImageField(upload_to='students/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'students'
        verbose_name = 'Student'
        verbose_name_plural = 'Students'
        indexes = [
            models.Index(fields=['email']),
            models.Index(fields=['roll_number']),
        ]

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

    def set_password(self, raw_password):
        """Hash and set the password."""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password is correct."""
        return check_password(raw_password, self.password)


class PasswordResetToken(models.Model):
    """Password reset tokens for all user types."""
    USER_TYPE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    ]

    email = models.EmailField(max_length=255)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    token = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    class Meta:
        db_table = 'password_reset_tokens'
        verbose_name = 'Password Reset Token'
        verbose_name_plural = 'Password Reset Tokens'
        indexes = [
            models.Index(fields=['token']),
            models.Index(fields=['email', 'user_type']),
        ]

    def __str__(self):
        return f"{self.user_type} - {self.email} - {self.token}"
