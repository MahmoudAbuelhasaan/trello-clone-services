# Trello Clone - Microservices Architecture

A complete Trello Clone application built with a modern microservices architecture using Django REST Framework, Docker, and various supporting services.

## 📋 Table of Contents

- [Project Overview](#project-overview)
- [Architecture](#architecture)
- [Services](#services)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Detailed Setup](#detailed-setup)
- [Running Services](#running-services)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Support](#support)

## 🎯 Project Overview

Trello Clone is a full-featured task management application inspired by Trello, built using a microservices architecture. It provides users with the ability to:

- Create and manage boards
- Organize tasks into lists
- Collaborate with team members
- Track project progress
- Manage user authentication

The application is designed for scalability, maintainability, and easy deployment using containerization.

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Client Applications                   │
│              (Web, Mobile, Desktop)                      │
└────────────────┬────────────────────────────────────────┘
                 │
        ┌────────▼────────┐
        │   API Gateway   │
        └────────┬────────┘
                 │
    ┌────────────┼────────────┐
    │            │            │
┌───▼────┐  ┌───▼────┐  ┌───▼────┐
│ Users  │  │ Boards │  │ Tasks  │
│Service │  │Service │  │Service │
└───┬────┘  └───┬────┘  └───┬────┘
    │           │           │
    └───────────┼───────────┘
                │
    ┌───────────┴───────────┐
    │                       │
┌───▼────┐         ┌───────▼──┐
│Database │         │Message Q │
│(PostgreSQL)       │(RabbitMQ)│
└────────┘         └─────┬────┘
                        │
                   ┌────▼─────┐
                   │  Celery  │
                   │  Workers │
                   └────┬─────┘
                        │
                   ┌────▼─────┐
                   │   Redis  │
                   │ (Caching)│
                   └──────────┘
```

## 📦 Services

### 1. **User Authentication Service** 🔐
- User registration and authentication
- JWT token management
- User profile management
- Email notifications

**Location**: `/users`
**Framework**: Django REST Framework
**Port**: 8000 (development)
**Documentation**: [User Service README](./users/README.md)

### 2. **Boards Service** (Planned) 📋
- Board creation and management
- Board sharing and permissions
- Board templates

**Location**: `/boards` (coming soon)

### 3. **Tasks Service** (Planned) ✅
- Task management
- Task assignment
- Task tracking and status updates
- Task comments and attachments

**Location**: `/tasks` (coming soon)

## 📋 Prerequisites

### System Requirements
- **OS**: Windows, macOS, or Linux
- **Docker**: 20.10+
- **Docker Compose**: 2.0+
- **Python**: 3.8+ (for local development)
- **Git**: 2.0+

### Optional (for local development without Docker)
- PostgreSQL 13+
- RabbitMQ 3.8+
- Redis 6.0+

## 🚀 Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Clone repository
git clone <repository-url>
cd trello-clone-services

# Start all services
docker compose up -d

# Run migrations
docker compose exec users python manage.py migrate

# Create superuser (optional)
docker compose exec users python manage.py createsuperuser
```

**Access Points:**
- User Service API: http://localhost:8000
- Swagger API Docs: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- Admin Panel: http://localhost:8000/admin/

### Option 2: Local Development

```bash
# Navigate to user service
cd users

# Create virtual environment
python -m venv env
source env/Scripts/activate  # Windows
# or
source env/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure .env file (see configuration section)

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver

# In another terminal, start Celery worker
celery -A users worker -l info
```

## ⚙️ Detailed Setup

### 1. Environment Variables

Create a `.env` file in the root directory:

```env
# Django Settings
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,127.0.0.1:3000

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=trello_auth
DB_USER=postgres
DB_PASSWORD=your-secure-password
DB_HOST=postgres-db
DB_PORT=5432

# Celery & Message Queue
CELERY_BROKER_URL=amqp://guest:guest@rabbitmq-service:5672//
CELERY_RESULT_BACKEND=redis://redis-service:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Redis Configuration
REDIS_URL=redis://redis-service:6379/0

# Logging
LOG_LEVEL=INFO
```

### 2. Docker Compose Configuration

The project includes a `docker-compose.yml` with the following services:

```yaml
Services:
- postgres-db          # PostgreSQL database
- rabbitmq-service     # Message broker
- redis-service        # Cache service
- users                # User authentication service
- celery-worker        # Async task processor
```

### 3. Database Setup

```bash
# Run migrations
docker compose exec users python manage.py migrate

# Create superuser
docker compose exec users python manage.py createsuperuser

# Load fixtures (if available)
docker compose exec users python manage.py loaddata fixtures/initial_data.json
```

## 🎬 Running Services

### Start All Services
```bash
docker compose up -d
```

### View Logs
```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f users
docker compose logs -f postgres-db
```

### Stop Services
```bash
docker compose down
```

### Restart Services
```bash
docker compose restart
```

### Remove Everything (including data)
```bash
docker compose down -v
```

## 📁 Project Structure

```
trello-clone-services/
├── users/                      # User authentication microservice
│   ├── accounts/              # User management app
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── serializers.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── tasks.py
│   │   └── tests.py
│   ├── users/                 # Project configuration
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── wsgi.py
│   │   ├── asgi.py
│   │   └── celery.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── manage.py
│   └── README.md
├── docker-compose.yml         # Docker orchestration
├── .env.example               # Environment template
├── .gitignore
└── README.md                  # This file
```

## 📚 API Documentation

### Interactive Documentation

Access the APIs through interactive Swagger/OpenAPI interfaces:

**User Service:**
- Swagger UI: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/
- OpenAPI JSON: http://localhost:8000/swagger.json

### Available Endpoints

#### User Authentication
```
POST   /api/v1/auth/register/          - Register new user
POST   /api/v1/auth/login/             - User login (token)
POST   /api/v1/auth/token/refresh/     - Refresh access token
GET    /api/v1/auth/profile/           - Get user profile
PUT    /api/v1/auth/profile/           - Update user profile
```

### API Response Format

**Success Response:**
```json
{
  "status": "success",
  "data": {
    // Response data
  },
  "message": "Operation completed successfully"
}
```

**Error Response:**
```json
{
  "status": "error",
  "error": {
    "code": "ERROR_CODE",
    "message": "Error description"
  }
}
```

## 💻 Development

### Local Development Setup

```bash
cd users

# Create virtual environment
python -m venv env
source env/Scripts/activate

# Install dependencies with dev packages
pip install -r requirements.txt

# Create .env file
cp .env.example .env

# Run migrations
python manage.py migrate

# Start development server
python manage.py runserver 0.0.0.0:8000
```

### Code Style & Linting

```bash
# Format code with Black
black .

# Run linting with Flake8
flake8 .

# Type checking with mypy
mypy .
```

### Testing

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

### Database Migrations

```bash
# Create new migration
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Rollback migration
python manage.py migrate accounts 0001
```

## 🚀 Deployment

### Production Checklist

- [ ] Set `DEBUG=False` in settings
- [ ] Configure `ALLOWED_HOSTS` properly
- [ ] Use strong `SECRET_KEY` from environment
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure email backend (SendGrid, AWS SES, etc.)
- [ ] Set up database backups
- [ ] Configure CDN for static files
- [ ] Set up monitoring and logging (ELK, Sentry)
- [ ] Configure rate limiting
- [ ] Set up CORS properly
- [ ] Use strong database passwords
- [ ] Enable security middleware
- [ ] Configure CI/CD pipeline

### Deployment Platforms

#### Docker Hub / Private Registry
```bash
# Build image
docker build -t trello-clone-users:latest users/

# Tag image
docker tag trello-clone-users:latest yourregistry/trello-clone-users:latest

# Push to registry
docker push yourregistry/trello-clone-users:latest
```

#### AWS ECS
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name trello-clone

# Push to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com

docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/trello-clone-users:latest
```

#### Heroku
```bash
# Login to Heroku
heroku login

# Create app
heroku create trello-clone-users

# Set environment variables
heroku config:set DEBUG=False SECRET_KEY=your-key -a trello-clone-users

# Deploy
git push heroku main
```

## 🧪 Testing

### Unit Tests
```bash
python manage.py test accounts.tests.UserModelTests
```

### Integration Tests
```bash
python manage.py test accounts.tests.RegistrationAPITests
```

### Load Testing
```bash
# Using locust
locust -f locustfile.py --host=http://localhost:8000
```

## 🔒 Security

### Implemented Security Features
- ✅ JWT authentication
- ✅ CSRF protection
- ✅ SQL injection prevention (ORM)
- ✅ XSS protection
- ✅ Password hashing (PBKDF2)
- ✅ Email validation
- ✅ Secure headers

### Recommendations
- Implement rate limiting
- Add CORS configuration
- Enable security middleware
- Regular dependency updates
- Security headers configuration

## 📊 Monitoring & Logging

### Logs
```bash
# View logs from all services
docker compose logs -f

# View specific service logs
docker compose logs -f users
```

### Health Checks
```bash
# User service health
curl http://localhost:8000/health/

# Database connection
docker compose exec users python manage.py dbshell
```

## 🐛 Troubleshooting

### Common Issues

**Port Already in Use**
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

**Database Connection Error**
```bash
# Check database is running
docker compose ps postgres-db

# Verify credentials in .env file
docker compose exec postgres-db psql -U postgres -d trello_auth
```

**Celery Tasks Not Processing**
```bash
# Check worker status
celery -A users inspect active

# Purge queue
celery -A users purge

# Restart worker
docker compose restart celery-worker
```

**Redis Connection Issues**
```bash
# Check redis is running
docker compose ps redis-service

# Test connection
docker compose exec redis-service redis-cli ping
```

## 📝 Contributing

### Development Workflow

1. **Fork and Clone**
   ```bash
   git clone <your-fork-url>
   cd trello-clone-services
   ```

2. **Create Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Changes**
   - Follow PEP 8 style guide
   - Write tests for new features
   - Update documentation

4. **Commit Changes**
   ```bash
   git commit -m "feat: add your feature description"
   ```

5. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```

### Code Style Guidelines
- Follow PEP 8
- Use type hints
- Write docstrings
- Keep functions small and focused
- Write meaningful commit messages

### Testing Requirements
- Minimum 80% code coverage
- All tests must pass
- No breaking changes

## 📄 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

## 👥 Authors

- **Development Team** - Initial architecture and setup

## 🙏 Support

For support, please:
- Open an issue on GitHub
- Email: support@trelloclone.com
- Check existing documentation

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Docker Documentation](https://docs.docker.com/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Celery Documentation](https://docs.celeryproject.org/)

## 🗺️ Roadmap

### Phase 1 (Current)
- ✅ User authentication service
- ⏳ API documentation and Swagger

### Phase 2 (Upcoming)
- ⏳ Boards service
- ⏳ Tasks service
- ⏳ Real-time notifications
- ⏳ WebSocket support

### Phase 3 (Future)
- ⏳ Team collaboration features
- ⏳ Analytics and reporting
- ⏳ Mobile app
- ⏳ Desktop app

## 📈 Performance Optimization

- Caching with Redis
- Database query optimization
- Connection pooling
- Async task processing
- Pagination for large datasets
- Gzip compression

---

**Last Updated**: January 31, 2026  
**Version**: 1.0.0  
**Status**: In Active Development
