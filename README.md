# Production-Grade Flask RESTful API

A scalable, production-ready RESTful API built with **Python**, **Flask**, **SQLAlchemy**, **Redis**, and **Docker**. Designed using software engineering best practices including the Application Factory pattern, JWT authentication, caching strategies, unit testing with Pytest, and full containerization.

---

## 🏗️ Architecture & Features

- **Application Factory Pattern**: Clean modular architecture using Flask Blueprints.
- **Database & ORM**: PostgreSQL (Production) / SQLite (Local Dev) managed with SQLAlchemy & Alembic migrations.
- **Authentication & Authorization**: Stateless JWT authentication with `Flask-JWT-Extended` and role-based authorization.
- **Caching**: In-memory caching with **Redis** for performant read-heavy endpoints.
- **Testing**: Automated unit and integration test suite using **Pytest**.
- **Containerization**: Fully containerized using **Docker** and **Docker Compose**.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.11+, Flask 3.x
- **Database**: PostgreSQL / SQLite, Flask-SQLAlchemy, Flask-Migrate
- **Caching**: Redis
- **Auth**: JWT (JSON Web Tokens)
- **Testing**: Pytest
- **DevOps**: Docker, Docker Compose

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional for containerized run)

### Local Setup (Without Docker)

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/your-username/flask-portfolio-api.git](https://github.com/your-username/flask-portfolio-api.git)
   cd flask-portfolio-api
   ```

2. **Create and activate virtual environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize Database:**
   ```bash
   flask db upgrade
   ```

5. **Run the Application:**
   ```bash
   python run.py
   ```
   The API will be available at `http://127.0.0.1:5000`.

---

## 🐳 Running with Docker

To launch the full stack (Flask API, PostgreSQL, and Redis) in containers:

```bash
docker-compose up --build
```

---

## 🧪 Running Tests

Execute the automated test suite using `pytest`:

```bash
python -m pytest tests/ -v
```

---

## 📌 API Endpoints

| Method | Endpoint | Description | Auth Required |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Server health check | No |
| `POST` | `/api/auth/register` | Register new user | No |
| `POST` | `/api/auth/login` | User login & JWT issuance | No |
| `GET` | `/api/auth/me` | Fetch user profile | Yes (JWT) |
| `GET` | `/api/items/` | Fetch items (Redis Cached) | No |
| `POST` | `/api/items/` | Create a new item | Yes (JWT) |
| `DELETE`| `/api/items/<id>` | Delete an item | Yes (Owner/Admin) |