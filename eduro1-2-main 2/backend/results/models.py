from django.db import models


class Result(models.Model):
    """Result model for storing student marks and grades."""
    GRADE_CHOICES = [
        ('A+', 'A+ (90-100%)'),
        ('A', 'A (80-89%)'),
        ('B+', 'B+ (70-79%)'),
        ('B', 'B (60-69%)'),
        ('C', 'C (50-59%)'),
        ('D', 'D (40-49%)'),
        ('F', 'F (0-39%)'),
    ]

    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE, related_name='results')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='results')
    internal_marks = models.FloatField(default=0)
    external_marks = models.FloatField(default=0)
    total_marks = models.FloatField(default=0)
    max_internal = models.IntegerField(default=30)
    max_external = models.IntegerField(default=70)
    max_total = models.IntegerField(default=100)
    percentage = models.FloatField(default=0)
    grade = models.CharField(max_length=2, choices=GRADE_CHOICES, blank=True)
    is_published = models.BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    entered_by_teacher = models.ForeignKey('authentication.Teacher', on_delete=models.SET_NULL, null=True, related_name='entered_results')
    approved_by_admin = models.ForeignKey('authentication.AdminUser', on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_results')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'results'
        verbose_name = 'Result'
        verbose_name_plural = 'Results'
        unique_together = [['student', 'subject']]
        indexes = [
            models.Index(fields=['student', 'is_published']),
            models.Index(fields=['subject', 'is_published']),
        ]

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.grade}"

    def calculate_grade(self):
        """Calculate grade based on percentage using standard 10-point grading scale."""
        if self.percentage >= 90:
            return 'A+'
        elif self.percentage >= 80:
            return 'A'
        elif self.percentage >= 70:
            return 'B+'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

    def save(self, *args, **kwargs):
        """Override save to automatically calculate total, percentage, and grade."""
        self.total_marks = self.internal_marks + self.external_marks
        self.percentage = (self.total_marks / self.max_total) * 100
        self.grade = self.calculate_grade()
        super().save(*args, **kwargs)
