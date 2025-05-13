# ✅ Task Tracker API - Task 06

A simple and powerful API for managing **Users** and their **Tasks**, built with **FastAPI** and **Pydantic** for data validation.

## 📦 Overview

This project implements a RESTful API to:

- Create and retrieve users
- Create, retrieve, and update tasks
- Assign tasks to users
- Enforce validation rules using Pydantic

---

## 🚀 Features

### ✅ Pydantic Models & Validation

- **UserCreate & UserRead** models based on `BaseModel`
- Email validation using `EmailStr`
- Username constrained to 3–20 characters using `constr`
- Task `due_date` must be today or later (validated with `@validator`)

---

## 🔌 FastAPI Endpoints

### 👤 Users

| Method | Endpoint           | Description               |
|--------|--------------------|---------------------------|
| POST   | `/users/`          | Create a new user         |
| GET    | `/users/{user_id}` | Retrieve a user by ID     |

### 📋 Tasks

| Method | Endpoint                     | Description                                  |
|--------|------------------------------|----------------------------------------------|
| POST   | `/tasks/`                    | Create a new task                            |
| GET    | `/tasks/{task_id}`           | Retrieve a task by ID                        |
| PUT    | `/tasks/{task_id}`           | Update the status of a task (validated)      |
| GET    | `/users/{user_id}/tasks`     | List all tasks assigned to a specific user   |

---

## 🛠️ Validation Rules

- `email`: must be a valid email address
- `username`: 3 to 20 characters only
- `due_date`: must be today or a future date
- `status` (for updates): only allowed values (e.g., `pending`, `in_progress`, `completed`)

---

## Install Dependencies

- pip install fastapi uvicorn pydantic

## Run the App

uvicorn main:app --reload






