**FastAPI Dependency Injection:**
**Overview:**

This project demonstrates Dependency Injection (DI) in FastAPI.
Dependency Injection allows us to share reusable logic across different API endpoints, promoting code reusability, separation of concerns, and easy testing.

**We will learn Dependency Injection through four examples:**

**Hello Dependency:** A simple dependency that returns a predefined goal.

**Dependency with Parameters:** Using dependencies with parameters, like passing a username to fetch the goal.

**Dependency with Query Parameters:** A simple login mechanism using query parameters.

**Multiple Dependencies:** Using multiple dependencies to perform different tasks.

**Using Classes as Dependencies:** Simulating a database with a class-based dependency.

**FastAPI Installation**:
uv init fastdca_p1
cd fastdca_p1
uv venv
source .venv/bin/activate
uv add "fastapi[standard]"

**Run the Application**
uvicorn main:app --reload
