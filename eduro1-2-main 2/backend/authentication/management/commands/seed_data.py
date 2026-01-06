from django.core.management.base import BaseCommand
from authentication.models import AdminUser, Teacher, Student
from academic.models import Department, Course, Semester, Subject, TeacherSubjectAssignment
from attendance.models import Attendance
from results.models import Result
from communications.models import Event, Announcement
from datetime import date, time, timedelta


class Command(BaseCommand):
    help = 'Seed database with demo data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding data...')

        # Create Department
        dept_cs, _ = Department.objects.get_or_create(
            code='CS',
            defaults={'name': 'Computer Science'}
        )

        # Create Course
        course, _ = Course.objects.get_or_create(
            department=dept_cs,
            name='B.Tech Computer Science',
            defaults={'duration_years': 4}
        )

        # Create Semester
        semester, _ = Semester.objects.get_or_create(
            course=course,
            semester_number=3,
            academic_year='2024-2025'
        )

        # Create Subjects
        subjects = []
        subject_names = [
            ('CS301', 'Data Structures', 4),
            ('CS302', 'Database Systems', 4),
            ('CS303', 'Operating Systems', 4),
            ('CS304', 'Computer Networks', 4),
            ('CS305', 'Web Technologies', 3),
        ]

        for code, name, credits in subject_names:
            subj, _ = Subject.objects.get_or_create(
                code=code,
                defaults={'semester': semester, 'name': name, 'credits': credits}
            )
            subjects.append(subj)

        # Create Admin
        admin, created = AdminUser.objects.get_or_create(
            email='admin@sims.edu',
            defaults={'full_name': 'System Admin', 'phone': '1234567890'}
        )
        if created:
            admin.set_password('admin123')
            admin.save()
            self.stdout.write(self.style.SUCCESS('Created admin: admin@sims.edu / admin123'))

        # Create Teacher
        teacher, created = Teacher.objects.get_or_create(
            email='teacher@sims.edu',
            defaults={
                'full_name': 'Dr. John Smith',
                'phone': '9876543210',
                'employee_id': 'T001',
                'department': dept_cs
            }
        )
        if created:
            teacher.set_password('teacher123')
            teacher.save()
            self.stdout.write(self.style.SUCCESS('Created teacher: teacher@sims.edu / teacher123'))

        # Assign subjects to teacher
        for subj in subjects[:3]:
            TeacherSubjectAssignment.objects.get_or_create(
                teacher=teacher,
                subject=subj
            )

        # Create Student
        student, created = Student.objects.get_or_create(
            email='student@sims.edu',
            defaults={
                'full_name': 'Alice Johnson',
                'phone': '5551234567',
                'roll_number': 'CS2021001',
                'semester': semester,
                'enrollment_year': '2021'
            }
        )
        if created:
            student.set_password('student123')
            student.save()
            self.stdout.write(self.style.SUCCESS('Created student: student@sims.edu / student123'))

        # Create Attendance records
        today = date.today()
        for i in range(10):
            att_date = today - timedelta(days=i)
            for subj in subjects[:3]:
                Attendance.objects.get_or_create(
                    student=student,
                    subject=subj,
                    teacher=teacher,
                    date=att_date,
                    lecture_time=time(9, 0),
                    defaults={'status': 'PRESENT' if i % 3 != 0 else 'ABSENT'}
                )

        # Create Results
        for subj in subjects[:3]:
            Result.objects.get_or_create(
                student=student,
                subject=subj,
                defaults={
                    'internal_marks': 25,
                    'external_marks': 60,
                    'is_published': True,
                    'entered_by_teacher': teacher,
                    'approved_by_admin': admin
                }
            )

        # Create Events
        Event.objects.get_or_create(
            title='Annual Tech Fest',
            defaults={
                'description': 'Three-day technical festival with competitions and workshops',
                'event_date': today + timedelta(days=15),
                'event_time': time(9, 0),
                'category': 'CULTURAL',
                'visibility': 'ALL',
                'created_by_admin': admin
            }
        )

        # Create Announcements
        Announcement.objects.get_or_create(
            title='Semester Exams Schedule Released',
            defaults={
                'content': 'The examination schedule for Semester 3 has been released. Please check the notice board.',
                'announcement_type': 'EXAM_ALERT',
                'visibility': 'ALL',
                'is_pinned': True,
                'created_by_admin': admin
            }
        )

        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))
