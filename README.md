# Library Management System

## Project Overview
The **Library Management System** is a Django-based application that allows users to browse, borrow, and return books.
It provides an API for managing books and loans, user authentication using JWT, and an admin panel for administrators.

## Features
- **User Registration & Authentication** (JWT-based)
- **Book Management** (Create, Read, Update, Delete)
- **Loan System** (Borrow & Return Books)
- **Search & Filter Books**
- **Overdue Loan Restrictions**
- **REST API Endpoints**
- **Django Admin Panel for Management**

---

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your-repo/library-management.git
cd library-management
```

### 2. Create and Activate a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the root directory:
```
SECRET_KEY=your-secret-key
DEBUG=True
```

### 5. Run Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create a Superuser
```bash
python manage.py createsuperuser
```

### 7. Start the Development Server
```bash
python manage.py runserver
```

---

## Project Structure
```
library_main/       # Main Django project
│── library/        # Library app
│   ├── migrations/ # Database migrations
│   ├── models.py   # Database models
│   ├── views.py    # API views
│   ├── serializers.py  # API serializers
│   ├── urls.py     # API routes
│   ├── admin.py    # Admin panel configurations
│   ├── tests.py    # Unit tests
│── library_main/   # Main project settings
│   ├── settings.py # Django settings
│   ├── urls.py     # Main project routes
│   ├── wsgi.py     # WSGI entry point
│   ├── asgi.py     # ASGI entry point
│── manage.py       # Django management script
│── requirements.txt  # Dependencies
```

---

## File & Function Descriptions

### `models.py` (Database Models)
- `Book`: Represents books in the library.
- `Loan`: Tracks book borrowing with return dates and overdue status.

### `admin.py` (Admin Panel Configuration)
- `BookAdmin`: Manages book listings.
- `LoanAdmin`: Manages loan records.

### `serializers.py` (Data Serialization)
- `BookSerializer`: Serializes books.
- `LoanSerializer`: Serializes loan records.
- `UserSerializer`: Handles user registration.

### `views.py` (API Views & Business Logic)
- `BookViewSet`: Fetch, search, and filter books.
- `LoanViewSet`: Fetch and manage loan records.
- `RegisterView`: Handles user registration.
- `borrow_book`: Custom function for borrowing books.

### `urls.py` (API Routes)
- `/books/` - Book list (GET, POST)
- `/loans/` - Loan list (GET, POST)
- `/register/` - User registration (POST)
- `/login/` - JWT login (POST)
- `/borrow_book/<book_id>/` - Borrow a book (POST)

### `tests.py` (Automated Tests)
Contains unit tests for:
- User registration and login.
- Book searching.
- Borrowing and returning books.
- Overdue loan detection.

Run tests using:
```bash
python manage.py test
```

### `settings.py` (Django Configuration)
Configures:
- Installed apps (`rest_framework`, `corsheaders`).
- Authentication (`JWT` settings).
- Database connection (`SQLite` or PostgreSQL`).
- Middleware (`whitenoise` for static files`).
- Allowed hosts and CORS settings.

### `wsgi.py` & `asgi.py` (Deployment Entry Points)
- `wsgi.py`: Used for **WSGI-based deployment** (e.g., Gunicorn).
- `asgi.py`: Used for **ASGI-based deployment** (e.g., WebSockets).

### `manage.py` (Django CLI Script)
Used for running Django commands like migrations, creating superusers, and running the server.

### `requirements.txt` (Dependencies)
Contains the required Python packages:
- `Django`
- `djangorestframework`
- `djangorestframework_simplejwt`
- `whitenoise` (for static files)
- `psycopg2` (PostgreSQL support)

Install dependencies using:
```bash
pip install -r requirements.txt
```

---

## Authentication & Borrowing Flow
1. **Register a User** (`POST /api/library/register/`)
2. **Login & Get JWT Token** (`POST /api/library/login/`)
3. **Search for a Book** (`GET /api/library/books/?search=Harry Potter`)
4. **Borrow a Book** (`POST /api/library/borrow_book/<book_id>/`)
5. **Return a Book** (`PATCH loan.return_book()` method)

---

## Deployment
To deploy, use **Gunicorn & Whitenoise** for static files.
Example deployment steps:
```bash
pip install gunicorn
gunicorn library_main.wsgi:application --bind 0.0.0.0:8000
```

---

## License
This project is licensed under the **MIT License**.

---

This README provides a comprehensive guide to the **Library Management System**. Let me know if you need modifications! 🚀
