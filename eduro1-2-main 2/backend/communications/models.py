from django.db import models


class Event(models.Model):
    """Event model for institute events."""
    CATEGORY_CHOICES = [
        ('ACADEMIC', 'Academic'),
        ('SPORTS', 'Sports'),
        ('CULTURAL', 'Cultural'),
        ('EXAM', 'Examination'),
        ('HOLIDAY', 'Holiday'),
        ('OTHER', 'Other'),
    ]

    VISIBILITY_CHOICES = [
        ('ALL', 'All Users'),
        ('TEACHERS_ONLY', 'Teachers Only'),
        ('STUDENTS_ONLY', 'Students Only'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    event_date = models.DateField()
    event_time = models.TimeField(blank=True, null=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='ALL')
    created_by_admin = models.ForeignKey('authentication.AdminUser', on_delete=models.CASCADE, related_name='created_events')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'events'
        verbose_name = 'Event'
        verbose_name_plural = 'Events'
        indexes = [
            models.Index(fields=['event_date']),
            models.Index(fields=['category']),
        ]
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return f"{self.title} - {self.event_date}"


class Announcement(models.Model):
    """Announcement model for important notices."""
    TYPE_CHOICES = [
        ('NOTICE', 'Notice'),
        ('EXAM_ALERT', 'Exam Alert'),
        ('HOLIDAY', 'Holiday'),
        ('URGENT', 'Urgent'),
        ('GENERAL', 'General'),
    ]

    VISIBILITY_CHOICES = [
        ('ALL', 'All Users'),
        ('TEACHERS_ONLY', 'Teachers Only'),
        ('STUDENTS_ONLY', 'Students Only'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField()
    announcement_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    visibility = models.CharField(max_length=20, choices=VISIBILITY_CHOICES, default='ALL')
    is_pinned = models.BooleanField(default=False)
    created_by_admin = models.ForeignKey('authentication.AdminUser', on_delete=models.CASCADE, related_name='created_announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'announcements'
        verbose_name = 'Announcement'
        verbose_name_plural = 'Announcements'
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_pinned']),
        ]
        ordering = ['-is_pinned', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.announcement_type})"
