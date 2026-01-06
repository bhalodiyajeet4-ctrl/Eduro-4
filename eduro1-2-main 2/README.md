# Smart Institute Management System (SIMS)

## Overview
A comprehensive web-based College/Institute Management System designed to centralize academic, administrative, and communication operations. Built as a final-year academic project, SIMS reduces manual work, improves transparency, supports real-time updates, and provides analytics-based insights for institutional decision-making.

## Features

### User Roles
- **Admin**: Full system control - manage users, approve results, create events, view analytics
- **Teacher**: Mark attendance, enter results, view student performance, manage assigned subjects
- **Student**: View attendance, check results, see announcements and events

### Core Modules
1. **Authentication System**
   - Three separate login portals (Admin, Teacher, Student)
   - JWT token-based authentication
   - Password reset functionality
   - Role-based access control

2. **Attendance Management**
   - Lecture-wise attendance tracking
   - Real-time percentage calculation
   - 24-hour edit window for corrections
   - Subject-wise and overall attendance reports
   - Low attendance alerts

3. **Result Management**
   - Internal + External marks entry (30 + 70 system)
   - Automatic grade calculation (A+ to F)
   - Teacher entry → Admin approval workflow
   - Real-time result publishing
   - Downloadable marksheets (PDF)

4. **Academic Structure Management**
   - Departments, Courses, Semesters, Subjects
   - Teacher-Subject assignments
   - Student enrollment management
   - Credit system for subjects

5. **Communication System**
   - Event management with categories (Academic, Sports, Cultural, Exam, Holiday)
   - Announcement system with visibility controls
   - Pinned announcements for urgent notices
   - Real-time notifications (WebSocket + polling fallback)

6. **Dashboard & Analytics**
   - Role-specific dashboards
   - Attendance trends (charts and graphs)
   - Result distribution analytics
   - Performance comparison
   - Quick action panels

7. **Reporting & Export**
   - PDF generation (marksheets, attendance reports, result reports)
   - Excel export (bulk data export)
   - Date-range filtering
   - Department/semester filtering

## Technology Stack

### Backend
- **Framework**: Django 4.2.7
- **API**: Django REST Framework 3.14.0
- **Authentication**: Django REST Framework SimpleJWT 5.3.0
- **Database**: SQLite (development), MySQL/PostgreSQL compatible
- **Real-time**: Django Channels 4.0.0 (WebSocket support)
- **CORS**: Django CORS Headers 4.3.0
- **PDF Generation**: ReportLab 4.0.7
- **Excel Export**: openpyxl 3.1.2
- **Image Handling**: Pillow 10.1.0

### Frontend (Planned)
- **Framework**: React 18+
- **Routing**: React Router DOM
- **HTTP Client**: Axios
- **Charts**: Chart.js / Recharts
- **Styling**: Custom CSS with responsive design

## Quick Start

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   python manage.py migrate
   ```

4. **Start development server**
   ```bash
   python manage.py runserver
   ```
   Backend runs on `http://localhost:8000`

## Database Schema Highlights

### Key Models Implemented
- **AdminUser, Teacher, Student**: Three separate user authentication models
- **Department → Course → Semester → Subject**: Hierarchical academic structure
- **TeacherSubjectAssignment**: Maps teachers to subjects they teach
- **Attendance**: Lecture-wise attendance with 24-hour edit window
- **Result**: Student marks with auto-calculated grades
- **Event, Announcement**: Communication and notices
- **Notification**: Real-time alerts with read/unread tracking

## Development Status

✅ **Phase 1 Completed (Backend Foundation):**
- Django project structure with 8 apps
- All database models implemented
- Database migrations completed
- Settings configured (CORS, JWT, Channels)
- Password hashing and authentication models ready

⏳ **In Progress:**
- Backend API implementation
- Frontend React application
- WebSocket notifications
- PDF/Excel report generation

📋 **Pending:**
- Complete REST API endpoints
- Frontend components and dashboards
- Integration testing
- Demo data seeding

See [IMPLEMENTATION_STATUS.md](IMPLEMENTATION_STATUS.md) for detailed progress tracking.

## Key Features Explained

### Attendance System
- **Lecture-wise tracking**: Each lecture tracked separately (date + time)
- **24-hour edit window**: Teachers can edit within 24 hours
- **Auto-calculations**: Attendance percentage calculated automatically
- **Low attendance alerts**: Students notified when below 75%

### Result System
- **Dual marking**: Internal (30 marks) + External (70 marks)
- **Auto-grading**: A+: 90-100%, A: 80-89%, B+: 70-79%, B: 60-69%, C: 50-59%, D: 40-49%, F: 0-39%
- **Two-step process**: Teacher enters → Admin publishes
- **Real-time notifications**: Students notified when results published

## Security Features

- **Password hashing**: Django's secure PBKDF2 hashing
- **JWT authentication**: 1-hour access tokens, 7-day refresh tokens
- **Role-based access**: Permission decorators enforce access control
- **CORS protection**: Configured for trusted origins only
- **Input validation**: Django ORM prevents SQL injection

## Project Structure

```
eduro1-2/
├── backend/
│   ├── authentication/       # User models and auth logic
│   ├── academic/             # Academic structure
│   ├── attendance/           # Attendance tracking
│   ├── results/              # Results and grading
│   ├── communications/       # Events and announcements
│   ├── notifications/        # Real-time notifications
│   ├── reports/              # PDF/Excel generation
│   ├── admin_management/     # Admin CRUD operations
│   ├── backend/              # Django settings
│   ├── manage.py
│   ├── requirements.txt
│   └── .env
│
└── frontend/                 # React app (to be implemented)
```

## Future Enhancements

- Multi-tenancy (multiple institutes)
- Mobile applications
- Email/SMS notifications
- Timetable management
- Library integration
- Fee management
- Online examinations
- Assignment submissions
- Biometric attendance
- ML-based analytics

## License

Academic Project - 2024-2025

---

**Built as a final-year academic project**
**Demonstrates: Full-stack development, REST APIs, Real-time communication, Database design, Authentication & Authorization**