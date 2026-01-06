from django.db import models


class Notification(models.Model):
    """Notification model for real-time alerts."""
    RECIPIENT_TYPE_CHOICES = [
        ('ADMIN', 'Admin'),
        ('TEACHER', 'Teacher'),
        ('STUDENT', 'Student'),
    ]

    NOTIFICATION_TYPE_CHOICES = [
        ('EVENT_REMINDER', 'Event Reminder'),
        ('RESULT_PUBLISHED', 'Result Published'),
        ('ATTENDANCE_LOW', 'Low Attendance Warning'),
        ('ANNOUNCEMENT', 'Announcement'),
        ('SYSTEM', 'System Notification'),
    ]

    recipient_type = models.CharField(max_length=10, choices=RECIPIENT_TYPE_CHOICES)
    recipient_id = models.IntegerField()  # ID of the admin/teacher/student
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    title = models.CharField(max_length=255)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    related_id = models.IntegerField(blank=True, null=True)  # Optional reference to related object
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'notifications'
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
        indexes = [
            models.Index(fields=['recipient_type', 'recipient_id', 'is_read']),
            models.Index(fields=['-created_at']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipient_type} {self.recipient_id} - {self.title}"
