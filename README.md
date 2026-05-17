# Dintern - Healthcare Application Backend

This repository contains a high-quality, production-ready healthcare backend system built with **Django**, **Django REST Framework (DRF)**, **Django ORM**, and **JWT Authentication** (via `djangorestframework-simplejwt`).

---

## 🎯 Objective
The goal of this assignment is to create a robust backend system for a healthcare application. The system securely handles user authentication, patient profiles, doctor records, and patient-doctor relationship mapping using clean and modular coding patterns.

---

## 🛠️ Technology Stack
* **Core Framework**: Django & Django REST Framework (DRF)
* **Authentication**: JWT (JSON Web Tokens) via `djangorestframework-simplejwt`
* **Database Modeling**: Django ORM
* **Local Database**: SQLite (fully compatible and easily swappable with PostgreSQL in `settings.py`'s `DATABASES`)
* **Environment Configuration**: `python-dotenv` for secure secret storage

---

## 🚀 Setup & Installation

### 1. Clone & Set up Virtual Environment
```bash
# Navigate to project directory
cd /Users/ishamadlani/dintern

# Activate virtual environment
source venv/bin/activate
```

### 2. Install Dependencies
```bash
pip install -r backend/requirements.txt
```

### 3. Database Migration
Generate and apply migrations using Django ORM to setup the database tables:
```bash
python backend/manage.py makemigrations doctors patients
python backend/manage.py migrate
```

### 4. Run Server
Start the Django development server on port `8000`:
```bash
python backend/manage.py runserver 8000
```

---

## 🗺️ API Documentation

All protected API endpoints require JWT authentication. Include your token in the request header using the **`Bearer`** prefix:
`Authorization: Bearer <your_access_token>`

### 🔐 1. Authentication APIs
* **`POST /api/auth/register/`**: Register a new user.
  * *Request Body*: `{"name": "Jane Doe", "email": "jane@example.com", "password": "securepassword123"}`
* **`POST /api/auth/login/`**: Authenticate credentials and retrieve access/refresh JWT tokens.
  * *Request Body*: `{"email": "jane@example.com", "password": "securepassword123"}`

---

### 🏥 2. Patient Management APIs (Authenticated)
* **`POST /api/patients/`**: Add a new patient record.
  * *Request Body*: `{"name": "John Doe", "age": 45, "condition": "Hypertension"}`
* **`GET /api/patients/`**: Retrieve all patients created by the authenticated user.
* **`GET /api/patients/<id>/`**: Get details of a specific patient by ID.
* **`PUT /api/patients/<id>/`**: Update patient profile details.
* **`DELETE /api/patients/<id>/`**: Delete a patient record.

---

### 👨‍⚕️ 3. Doctor Management APIs (Authenticated)
* **`POST /api/doctors/`**: Add a new doctor record.
  * *Request Body*: `{"name": "Dr. Sarah House", "specialty": "Neurology", "experience": 12}`
* **`GET /api/doctors/`**: Retrieve all doctors created by the authenticated user.
* **`GET /api/doctors/<id>/`**: Get details of a specific doctor.
* **`PUT /api/doctors/<id>/`**: Update doctor details.
* **`DELETE /api/doctors/<id>/`**: Delete a doctor record.

---

### 🔗 4. Patient-Doctor Mapping APIs (Authenticated)
* **`POST /api/mappings/`**: Assign a doctor to a patient.
  * *Request Body*: `{"patient_id": "PATIENT_UUID", "doctor_id": "DOCTOR_UUID"}`
* **`GET /api/mappings/`**: Retrieve all global patient-doctor name pairings (`patient_name` & `doctor_name` pairs from the whole DB).
* **`GET /api/mappings/<patient_id>/`**: Get the detailed profile of the doctor assigned to a specific patient.
* **`DELETE /api/mappings/<patient_id>/`**: Unassign a doctor from a patient (resets `doctor_id` to `NULL`).
