# Ai exam sitting arrangement system

This project is an AI-powered Exam Sitting Arrangement System designed to streamline exam management for universities and colleges. It automates seat allocations, invigilator assignments, leave management, result processing, and provides dashboards for admins, staff, and students

Built with Flask, SQLAlchemy ORM, JWT auth, and MySQL. Frontend scaffolded with React + Vite + Material UI.

---

## Project overview

- **Goal:**
  - Automate exam seating allocation using AI‑assisted logic (fairness, branch/year separation, room capacity).
  - Provide dashboards for Admin, Staff, and Students.
  - Streamline workflows: invigilation, leave requests, results, and notifications.
- **Roles:** Admin, Student, Staff.
- **Core capabilities (so far):**
  - **Auth:** Signup, login, JWT-protected profile using email identity.
  - **Admin:** Create/list exams, add rooms, list students.
  - **Database:** MySQL + SQLAlchemy with migrations (Flask-Migrate).

---

## Tech stack and architecture

- **Backend:** Flask, Flask-JWT-Extended, Flask-Migrate, SQLAlchemy, PyMySQL.
- **Frontend:** React + Vite + Material UI (scaffolded for later phases).
- **Database:** MySQL.
- **Architecture:** App factory pattern, blueprints per module, centralized extensions, environment-based config.
- **Key modules:**
  - **Extensions:** db, migrate, jwt, mail, cors.
  - **Models:** User, Exam, Room, Seat, Allocation, Invigilation, LeaveRequest.
  - **Routes:** auth, admin, student (planned), staff (planned).

---

## Current Milestones

**Phase 1: Auth & Setup**
- User signup/login with JWT tokens
- Role-based access control (ADMIN, STAFF, STUDENT)
  
**Phase 2: Exams & Rooms**
- Admin creates exams and rooms
- Admin lists exams and student
  
**Phase 3: Seats & Allocations**
- Seat model linked to rooms
- Admin allocates students to seats
- Students view their seat allocations
  
**Phase 4: Invigilations**
- Admin assigns staff to invigilate exams
- Staff view their invigilations
  
**Phase 5: Leave Management**
- Staff apply for leave
- Admin approves/rejects leave requests
- Staff view leave status
 
**Phase 6: Results & Performance**
- Admin uploads exam results
- Students view results and performance summaries (average marks, grades)
  
**Phase 7: Reports & Analytics**
- Admin dashboard: students, staff, exams, rooms, seats, allocations, leaves, results summary
- Staff dashboard: personal invigilations + leave summary
- Students already have performance view
  
**🔜 Phase 8–9 upcoming: AI seat allocation + mailer notifications + frontend dashboard**

## API Endpoints

**Auth**

- POST /api/auth/signup → Register user
- POST /api/auth/login → Login, get JWT
- GET /api/auth/me → Profile

**Admin**

- POST /api/admin/exam → Create exam
- GET /api/admin/exams → List exams
- POST /api/admin/room → Add room
- GET /api/admin/students → List students
- POST /api/admin/allocations → Allocate students to seats (AI logic planned)
- GET /api/admin/allocations → View allocations
- POST /api/admin/invigilation → Assign invigilators
- GET /api/admin/invigilations → List invigilations
- PATCH /api/admin/leave/<id>/status → Approve/reject leave
- GET /api/admin/leaves → View leave requests
- POST /api/admin/result → Upload results
- GET /api/admin/results/<exam_id> → View results for exam
- GET /api/admin/reports → Global dashboard

**Staff**

- GET /api/staff/invigilations → View invigilations
- POST /api/staff/leave → Apply for leave
- GET /api/staff/leaves → View leave requests
- GET /api/staff/reports → Personal dashboard

**Student**

- GET /api/student/allocations → View seat allocation
- GET /api/student/results → View exam results
- GET /api/student/performance → View performance summary

**AI Services (Planned Integration)**

- POST /api/admin/allocations/ai → Trigger AI‑assisted seat allocation (calls seating_ai.py)
- POST /api/admin/notify/allocations → Send seat allocation emails (calls mailer.py)
- POST /api/admin/notify/results → Send result emails (calls mailer.py)

## Setup and running locally

### Prerequisites

- **Tools:** Python 3.10+, Node.js (for frontend later), MySQL 8+.
- **OS:** Windows 11 (tested), PowerShell recommended.
- **Config:** MySQL user and password with permissions to create databases.

### Backend setup

1. **Clone repository**

   ```bash
   git clone https://github.com/1822lokesh/ai-exam-sitting.git
   cd ai-exam-sitting/backend
   ```

2. **Create and activate virtual environment**

   ```powershell
   python -m venv .venv
   . .venv\Scripts\activate
   ```

3. **Install dependencies**

   ```powershell
   pip install -r requirements.txt
   ```

4. **Create environment file**
   Create `backend/.env` with:

   ```dotenv
   SECRET_KEY=your-secret
   JWT_SECRET_KEY=your-jwt-secret
   SQLALCHEMY_DATABASE_URI=mysql+pymysql://<user>:<password>@localhost:3306/ai_exam
   FRONTEND_ORIGIN=http://127.0.0.1:5173
   MAIL_SERVER=smtp.example.com
   MAIL_PORT=587
   MAIL_USERNAME=your@email.com
   MAIL_PASSWORD=your-mail-password
   MAIL_USE_TLS=true
   ```

5. **Create database (MySQL)**

   ```sql
   CREATE DATABASE ai_exam;
   ```

6. **Register models in app factory**
   In `app/__init__.py` ensure:

   ```python
   from .models import user, exam, leave
   ```

7. **Run migrations**

   ```powershell
   $env:FLASK_APP = "wsgi.py"
   flask db init          # run once
   flask db migrate -m "Initial tables"
   flask db upgrade
   ```

8. **Run server**
   ```powershell
   flask run
   ```
   Server runs at `http://127.0.0.1:5000`.

### Frontend setup (scaffolded, optional for now)

- **Install and run dev server**
  ```bash
  cd ../frontend
  npm install
  npm run dev
  ```

---

## Testing walkthrough

### Authentication

- **Signup**

  ```http
  POST /api/auth/signup
  Content-Type: application/json
  {
    "name": "Admin User",
    "email": "admin@example.com",
    "password": "admin123",
    "role": "ADMIN"
  }
  ```

  - **Expected:** `201 { "message": "User created successfully" }`

- **Login**

  ```http
  POST /api/auth/login
  Content-Type: application/json
  {
    "email": "admin@example.com",
    "password": "admin123"
  }
  ```

  - **Expected:** `200 { "access_token": "<JWT>" }`
  - **Header for protected routes:** `Authorization: Bearer <JWT>`

- **Profile**
  ```http
  GET /api/auth/me
  Authorization: Bearer <JWT>
  ```
  - **Expected:** user details with id, name, email, role

### Admin APIs

- **Create exam**

  ```http
  POST /api/admin/exam
  Authorization: Bearer <JWT>
  Content-Type: application/json
  {
    "subject": "Mathematics",
    "semester": 5,
    "date": "2025-12-01",
    "start_time": "09:00:00",
    "end_time": "12:00:00"
  }
  ```

  - **Expected:** `201 { "message": "Exam created successfully" }`

- **List exams**

  ```http
  GET /api/admin/exams
  Authorization: Bearer <JWT>
  ```

  - **Expected:** array of exams

- **Add room**

  ```http
  POST /api/admin/room
  Authorization: Bearer <JWT>
  Content-Type: application/json
  {
    "name": "Room A",
    "benches_count": 20,
    "capacity": 40
  }
  ```

  - **Expected:** `201 { "message": "Room added successfully" }`

- **List students**
  ```http
  GET /api/admin/students
  Authorization: Bearer <JWT>
  ```
  - **Expected:** array of student records

---

## Project structure (backend)

---


---

## Development notes and troubleshooting

- **Password hash length:** Use `String(255)` or `Text` for `password_hash` to avoid overflow with scrypt hashes.
- **JWT identity:** Use email as identity (`create_access_token(identity=user.email)`) to avoid “Subject must be a string” errors.
- **Model discovery:** Ensure models are imported in `create_app()` before migrations; otherwise `db.metadata.tables` will be empty.
- **Flask shell checks:**
  - **List tables:**
    ```python
    from app.extensions import db
    print(db.metadata.tables.keys())
    ```
  - **Insert dummy user:**
    ```python
    from app.models.user import User
    from app.extensions import db
    u = User(name="Test", email="test@example.com", role="STUDENT"); u.set_password("password")
    db.session.add(u); db.session.commit()
    ```

---

## Roadmap

- **✅ Phase 1–7**: Backend system ready (auth, exams, rooms, seats, allocations, invigilations, leaves, results, reports)
- **🔜 Phase 8**: React dashboard UI (Admin/Student/Staff), role‑based navigation, API integration
- **🔜 Phase 9**: AI seat allocation logic (allocation.py + seating_ai.py) + mailer notifications (mailer.py)
- **🔜 Phase 10**: Deployment with Docker, environment configs, CI/CD, production hardening

---

## Contributing

- **Branching:** feature branches per module (e.g., `feature/student-routes`).
- **Commits:** clear messages per phase or feature.
- **PRs:** include tests and README updates for new endpoints.
