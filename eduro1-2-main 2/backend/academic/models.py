from django.db import models


class Department(models.Model):
    """Department model for organizing courses."""
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=20, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'departments'
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.name} ({self.code})"


class Course(models.Model):
    """Course model representing degree programs."""
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    name = models.CharField(max_length=255)
    duration_years = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'courses'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return f"{self.name} - {self.department.code}"


class Semester(models.Model):
    """Semester model for organizing subjects."""
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='semesters')
    semester_number = models.IntegerField()
    academic_year = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'semesters'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        unique_together = [['course', 'semester_number', 'academic_year']]
        indexes = [
            models.Index(fields=['academic_year']),
        ]

    def __str__(self):
        return f"Semester {self.semester_number} - {self.course.name} ({self.academic_year})"


class Subject(models.Model):
    """Subject model representing individual subjects."""
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=255)
    code = models.CharField(max_length=50, unique=True)
    credits = models.IntegerField(default=4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'subjects'
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
        indexes = [
            models.Index(fields=['code']),
        ]

    def __str__(self):
        return f"{self.code} - {self.name}"


class TeacherSubjectAssignment(models.Model):
    """Maps which teachers teach which subjects."""
    teacher = models.ForeignKey('authentication.Teacher', on_delete=models.CASCADE, related_name='subject_assignments')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='teacher_assignments')
    assigned_date = models.DateField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'teacher_subject_assignments'
        verbose_name = 'Teacher Subject Assignment'
        verbose_name_plural = 'Teacher Subject Assignments'
        unique_together = [['teacher', 'subject']]

    def __str__(self):
        return f"{self.teacher.full_name} - {self.subject.code}"
