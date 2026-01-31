# Trello Clone - User Authentication Service

A robust user authentication and management microservice built with Django REST Framework, JWT tokens, and Celery for the Trello Clone application.

## 📋 Table of Contents

- [Features](#features)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Application](#running-the-application)
- [API Documentation](#api-documentation)
- [Project Structure](#project-structure)
- [Database Models](#database-models)
- [Contributing](#contributing)

## ✨ Features

- **User Registration** - Create new user accounts with email validation
- **JWT Authentication** - Secure token-based authentication
- **User Profiles** - Extended user information and profile management
- **Password Validation** - Strong password requirements and validation
- **Welcome Emails** - Async email notifications using Celery
- **Swagger/OpenAPI** - Interactive API documentation
- **Docker Support** - Full containerization with Docker Compose
- **PostgreSQL Database** - Reliable data persistence
- **Message Queue** - RabbitMQ integration for async tasks
- **Caching** - Redis support for performance optimization

## 🛠 Tech Stack

- **Backend Framework**: Django 5.2 + Django REST Framework
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: drf-yasg (Swagger/OpenAPI)
- **Database**: PostgreSQL
- **Message Broker**: RabbitMQ
- **Task Queue**: Celery
- **Cache**: Redis
- **Containerization**: Docker & Docker Compose
- **Python**: 3.x

## 📦 Prerequisites

Before you begin, ensure you have installed:

- Docker & Docker Compose
- Python 3.8+ (if running locally)
- PostgreSQL (if not using Docker)
- RabbitMQ (if not using Docker)
- Redis (if not using Docker)

## 🚀 Installation

### Using Docker Compose (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd trello-clone-services

# Start all services
docker compose up -d

# The service will be available at http://localhost:8000
```

### Local Development Setup

1. **Create virtual environment**
   ```bash
   python -m venv env
   source env/Scripts/activate  # On Windows
   # or
   source env/bin/activate  # On macOS/Linux
   ```

2. **Install dependencies**
   ```bash
   cd users
   pip install -r requirements.txt
   ```

3. **Configure environment variables** (see Configuration section)

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

## ⚙️ Configuration

Create a `.env` file in the root directory with the following variables:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=trello_auth
DB_USER=postgres
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432

# Celery
CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//
CELERY_RESULT_BACKEND=redis://localhost:6379/0

# Email (Optional)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
```

## 🎯 Running the Application

### Development Mode
```bash
python manage.py runserver 0.0.0.0:8000
```

### Production Mode (Docker)
```bash
docker compose -f docker-compose.yml up -d
```

### Run Celery Worker (in separate terminal)
```bash
celery -A users worker -l info
```

### Run Celery Beat Scheduler (optional)
```bash
celery -A users beat -l info
```

## 📚 API Documentation

### Swagger/OpenAPI Interface

Access the interactive API documentation at:

- **Swagger UI**: http://localhost:8000/swagger/
- **ReDoc**: http://localhost:8000/redoc/
- **OpenAPI Schema**: http://localhost:8000/swagger.json

### Available Endpoints

#### User Registration
```
POST /api/v1/auth/register/
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "first_name": "John",
  "last_name": "Doe",
  "password": "SecurePassword123!",
  "password_confirm": "SecurePassword123!"
}
```

**Response (201 Created):**
```json
{
  "message": "User registered successfully.",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "username": "username",
    "first_name": "John",
    "last_name": "Doe"
  },
  "token": {
    "refresh": "eyJ...",
    "access": "eyJ..."
  }
}
```

#### Token Refresh
```
POST /api/v1/auth/token/refresh/
```

## 📁 Project Structure

```
users/
├── accounts/                 # User management app
│   ├── migrations/          # Database migrations
│   ├── models.py            # User & UserProfile models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # API views
│   ├── urls.py              # App URL routing
│   ├── tasks.py             # Celery tasks
│   └── admin.py             # Django admin configuration
├── users/                    # Project settings
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL routing
│   ├── asgi.py              # ASGI configuration
│   ├── wsgi.py              # WSGI configuration
│   └── celery.py            # Celery configuration
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
├── Dockerfile               # Container configuration
└── README.md               # This file
```

## 🗄️ Database Models

### User Model
- `id` - Primary key
- `email` - Unique email address
- `username` - Unique username
- `first_name` - User's first name
- `last_name` - User's last name
- `is_active` - Account activation status
- `created_at` - Account creation timestamp

### UserProfile Model
- `user` - ForeignKey to User
- `bio` - User biography
- `profile_picture` - Avatar image
- `updated_at` - Last update timestamp

## 🧪 Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## 🔒 Security Features

- ✅ JWT token-based authentication
- ✅ Password strength validation
- ✅ Email uniqueness validation
- ✅ CSRF protection
- ✅ Secure password hashing
- ✅ Rate limiting (can be added)
- ✅ CORS configuration (can be added)

## 🐛 Troubleshooting

### Database Connection Issues
```bash
# Reset database
python manage.py migrate zero accounts
python manage.py migrate

# Create fresh database
python manage.py flush
python manage.py migrate
```

### Celery Tasks Not Running
```bash
# Check if worker is running
celery -A users inspect active

# Flush task queue
celery -A users purge
```

### Port Already in Use
```bash
# Change port
python manage.py runserver 8001
```

## 📝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see LICENSE file for details.

## 👥 Support

For support, email support@example.com or create an issue in the repository.

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure allowed hosts
- [ ] Set strong `SECRET_KEY`
- [ ] Configure email backend
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Set up monitoring and logging
- [ ] Configure rate limiting
- [ ] Set up CORS properly

---

**Last Updated**: January 31, 2026


