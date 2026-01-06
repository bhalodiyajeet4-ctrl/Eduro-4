from django.db import models
from django.utils import timezone
from datetime import timedelta


class Attendance(models.Model):
    """Attendance model for tracking lecture-wise attendance."""
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]

    student = models.ForeignKey('authentication.Student', on_delete=models.CASCADE, related_name='attendance_records')
    subject = models.ForeignKey('academic.Subject', on_delete=models.CASCADE, related_name='attendance_records')
    teacher = models.ForeignKey('authentication.Teacher', on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField()
    lecture_time = models.TimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    marked_at = models.DateTimeField(auto_now_add=True)
    is_editable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        unique_together = [['student', 'subject', 'date', 'lecture_time']]
        indexes = [
            models.Index(fields=['date']),
            models.Index(fields=['student', 'date']),
            models.Index(fields=['subject', 'date']),
        ]

    def __str__(self):
        return f"{self.student.roll_number} - {self.subject.code} - {self.date} - {self.status}"

    def check_editability(self):
        """Check if attendance is still editable (within 24 hours)."""
        time_diff = timezone.now() - self.marked_at
        if time_diff > timedelta(hours=24):
            self.is_editable = False
            self.save()
        return self.is_editable
