# Ai exam sitting arrangement system

A backend-first project to automate exam seating, invigilation, and leave workflows with role-based access for Admin, Student, and Staff. Built with Flask, SQLAlchemy ORM, JWT auth, and MySQL. Frontend scaffolded with React + Vite + Material UI.

---

## Project overview

- **Goal:** Automate exam seating allocation and related operations with a clean, scalable architecture.
- **Roles:** Admin, Student, Staff.
- **Current milestone:** Phases 1–5 completed (backend setup, models, migrations, auth, admin APIs).
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

## Setup and running locally

### Prerequisites

- **Tools:** Python 3.10+, Node.js (for frontend later), MySQL 8+.
- **OS:** Windows 11 (tested), PowerShell recommended.
- **Config:** MySQL user and password with permissions to create databases.

### Backend setup

1. **Clone repository**

   ```bash
   git clone https://github.com/<your-username>/ai-exam-sitting.git
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

## Testing walkthrough (phases 4–5)

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

```
backend/
├─ app/
│  ├─ __init__.py          # app factory, extensions init, model imports, blueprint registration
│  ├─ config.py            # environment-based configuration
│  ├─ extensions.py        # db, migrate, jwt, mail, cors
│  ├─ models/
│  │  ├─ user.py
│  │  ├─ exam.py
│  │  ├─ room.py
│  │  ├─ seat.py
│  │  ├─ allocation.py
│  │  ├─ invigilation.py
│  │  └─ leave.py
│  ├─ routes/
│  │  ├─ auth.py
│  │  ├─ admin.py
│  │  ├─ student.py        # planned
│  │  └─ staff.py          # planned
│  └─ ...
├─ migrations/             # alembic migration scripts
├─ wsgi.py                 # entrypoint: app = create_app()
├─ requirements.txt
└─ .env
```

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

- **Phase 6:** Student routes (exam schedule, seat allocation view, leave requests).
- **Phase 7:** Staff routes (invigilation assignments, approve/deny leave).
- **Phase 8:** React dashboard UI (Admin/Student/Staff), role-based navigation, API integration.
- **Phase 9:** Seat allocation logic (AI-assisted), constraints (branch, year, room capacity).
- **Phase 10:** Deployment with Docker, environment configs, CI/CD, production hardening.

---

## Contributing

- **Branching:** feature branches per module (e.g., `feature/student-routes`).
- **Commits:** clear messages per phase or feature.
- **PRs:** include tests and README updates for new endpoints.







