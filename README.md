# 📚 Library Management API

A clean, modular backend system for managing library operations built using **FastAPI**, **PostgreSQL**, and **SQLAlchemy**, supporting dual-mode authentication (JWT & API Key), role-based access control, and rate-limited API endpoints.

---

## 🚀 Tech Stack

- **FastAPI** – modern async Python web framework
- **PostgreSQL** – relational database
- **SQLAlchemy ORM** – database models
- **Pydantic v2** – request/response validation
- **JWT Authentication** – secure, stateless login
- **API Key Authentication** – for persistent tokens
- **Rate Limiting** – using `slowapi`
- **Modular Layers** – API ➞ Service ➞ Repository ➞ DB
- **Docker** – containerized deployment

---

## 📂 Project Structure

```bash
library_management_backend/
│
├── app/
│   ├── api/                # API routes
│   ├── core/               # Config, security, rate limiting
│   ├── db/                 # DB models, session, base
│   ├── schemas/            # Pydantic schemas
│   ├── services/           # Business logic
│   ├── repositories/       # DB queries
│   └── utils/              # Logging, error handling
│
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Multi-container Docker config
├── requirements.txt
├── main.py                 # App entrypoint
└── README.md               # You are here!
```

---

## 🔐 Authentication

Supports **dual-mode authentication**:

| Method     | Header Key         | Description                  |
|------------|--------------------|------------------------------|
| JWT Token  | `Authorization: Bearer <token>` | Issued at login/registration |
| API Key    | `X-API-Key: <key>` | Unique per user, persistent  |

---

## 🧑‍💼 User Roles

- **Librarian** – full access (add/update/delete books, view user history)
- **User** – can borrow/return books, view own history

---

## 📌 Core API Endpoints

### 🔑 Authentication

| Method | Endpoint         | Description                     |
|--------|------------------|---------------------------------|
| POST   | `/auth/register` | Register user, returns JWT + API key |
| POST   | `/auth/login`    | Login, returns JWT + API key    |

---

### 📚 Book Management

| Method | Endpoint             | Access     | Description              |
|--------|----------------------|------------|--------------------------|
| POST   | `/books/`            | Librarian  | Add a new book           |
| PUT    | `/books/{id}`        | Librarian  | Update book details      |
| GET    | `/books/search`      | Auth users | Filter + paginate books  |

---

### ⟻ Borrowing

| Method | Endpoint               | Access     | Description                   |
|--------|------------------------|------------|-------------------------------|
| POST   | `/borrow/{book_id}`    | User       | Borrow a book                 |
| POST   | `/return/{book_id}`    | User       | Return a borrowed book        |
| GET    | `/history/me`          | User       | View own borrow history       |
| GET    | `/history/{user_id}`   | Librarian  | View any user's history       |

---

## 🧪 Rate Limiting

Powered by **slowapi**:

- `/books/search` → `10/minute`
- `/auth/register` → `5/minute`
- `/borrow` + `/return` → `3/minute`

You can modify this in individual routes using:

```python
@limiter.limit("5/minute")
```

---

## 🛠️ Setup & Run Locally

1. **Clone repo & install dependencies**

   ```bash
   git clone https://github.com/rramees/library_management_backend.git
   cd library_management_backend
   pip install -r requirements.txt
   ```

2. **Set environment variables**

   Create a `.env` file in `app/core/`:

   ```env
   DATABASE_URL=postgresql://user:password@localhost/library_db
   SECRET_KEY=your-secret
   ALGORITHM=HS256
   ```

3. **Run the server**

   ```bash
   uvicorn app.main:app --reload
   ```

---

## 🐳 Running with Docker

1. **Build and start the containers**

   ```bash
   docker-compose up --build
   ```

   This will start both the FastAPI application and PostgreSQL database.

2. **Access the API**

   The API will be available at:

   ```bash
   http://localhost:8000
   ```

3. **Stopping the containers**

   ```bash
   docker-compose down
   ```

4. **Reset the database**

   To completely reset the database, including its volume:

   ```bash

   docker-compose down -v
   ```

---

## 📘 Swagger API Docs

Available at:

```bash
http://localhost:8000/docs
```

Or ReDoc at:

```bash
http://localhost:8000/redoc
```

---
