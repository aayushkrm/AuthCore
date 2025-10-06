# Custom Authentication & Authorization System

A production-ready Django REST Framework implementation of custom authentication and authorization with granular role-based access control (RBAC), built entirely from scratch without using Django's built-in authentication framework.

## 🎯 Project Overview

This system demonstrates advanced backend development skills by implementing:
- **Custom JWT Authentication** - Token-based authentication without Django's auth framework
- **Bcrypt Password Hashing** - Industry-standard secure password storage
- **Granular RBAC** - 7 distinct permission types per resource
- **Custom Middleware** - Request-level user identification
- **Ownership-based Access Control** - Users can only access their own resources
- **Admin API** - Dynamic permission management system
- **Soft Delete** - Data integrity preservation

## ✨ Key Features

### Authentication
- User registration with email validation
- JWT token generation and validation
- Password hashing with bcrypt + salt
- Token expiration (24-hour default)
- Session management
- Soft delete (account deactivation)

### Authorization
- Role-based access control (admin, manager, user, guest)
- 7 permission types: read, read_all, create, update, update_all, delete, delete_all
- Ownership-based permissions (users vs. all objects)
- Dynamic access rule management
- Permission hierarchy system

### Security
- Custom middleware for authentication
- No exposure of Django's built-in auth
- Proper HTTP status codes (401, 403, 404)
- SQL injection prevention via ORM
- CSRF protection
- Environment-based configuration

## 🗄️ Database Schema

### Core Tables

**users** - User accounts and authentication
```markdown
- id (PK)
- email (unique, indexed)
- first_name, last_name, patronymic
- password_hash (bcrypt)
- is_active (for soft delete)
- created_at, updated_at
```

**roles** - System roles
```markdown
- id (PK)
- name (admin, manager, user, guest)
- description
```

**user_roles** - User-role assignments (many-to-many)
```markdown
- id (PK)
- user_id (FK → users)
- role_id (FK → roles)
- assigned_at
```

**business_elements** - Protected resources
```markdown
- id (PK)
- name (products, users, orders, stores, access_rules)
- description
```

**access_roles_rules** - Permission matrix
```markdown
- id (PK)
- role_id (FK → roles)
- element_id (FK → business_elements)
- read_permission, read_all_permission
- create_permission
- update_permission, update_all_permission
- delete_permission, delete_all_permission
```

**sessions** - Session management (optional)
```markdown
- id (PK)
- user_id (FK → users)
- session_id (unique)
- expire_at
- created_at
```

### Relationships
```

users 1---* user_roles *---1 roles
roles 1---* access_roles_rules *---1 business_elements
users 1---* sessions

```

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- PostgreSQL 12 or higher
- pip and virtualenv

### Installation

**1. Clone and Navigate**
```

cd auth_system

```

**2. Create Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows
```

**3. Install Dependencies**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**4. Configure Environment**
```bash
cp .env.example .env
```

Edit `.env` with your settings:
```ini
SECRET_KEY=your-django-secret-key
JWT_SECRET=your-jwt-secret-key
DB_NAME=auth_system_db
DB_USER=your_username
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

**Generate secret keys:**
```


# Django SECRET_KEY

python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# JWT_SECRET

python3 -c "import secrets; print(secrets.token_urlsafe(50))"

```

**5. Create Database**
```


# Option 1: Using createdb

createdb auth_system_db

# Option 2: Using psql

psql postgres
CREATE DATABASE auth_system_db;
\q

```

**6. Run Migrations**
```

python manage.py makemigrations
python manage.py migrate

```

**7. Seed Test Data**
```

python manage.py seed_data

```

**8. Start Server**
```

python manage.py runserver

```

Server will be available at: `http://localhost:8000`

### Test the API

**Login:**
```

curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "admin@test.com", "password": "password123"}'

```

**Use Token (replace TOKEN with response):**
```

TOKEN="your_token_here"

curl http://localhost:8000/api/products/ \
-H "Authorization: Bearer \$TOKEN"

```

## 🔑 Test Accounts

All passwords: `password123`

| Email | Role | Access Level |
|-------|------|--------------|
| admin@test.com | Admin | Full system access |
| manager@test.com | Manager | Extended permissions |
| user1@test.com | User | Basic user access |
| user2@test.com | User | Basic user access |
| guest@test.com | Guest | Read-only access |
| inactive@test.com | Inactive | Cannot login (deactivated) |

## 📡 API Endpoints

### Authentication

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register/` | Register new user | No |
| POST | `/api/auth/login/` | Login (get JWT token) | No |
| GET | `/api/auth/profile/` | Get current user | Yes |
| PUT | `/api/auth/profile/` | Update profile | Yes |
| PATCH | `/api/auth/profile/` | Partial update | Yes |
| POST | `/api/auth/logout/` | Logout user | Yes |
| DELETE | `/api/auth/delete-account/` | Soft delete account | Yes |

### Authorization (Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/access-rules/` | List all access rules |
| POST | `/api/access-rules/` | Create access rule |
| GET | `/api/access-rules/{id}/` | Get specific rule |
| PUT | `/api/access-rules/{id}/` | Update rule |
| PATCH | `/api/access-rules/{id}/` | Partial update |
| DELETE | `/api/access-rules/{id}/` | Delete rule |
| GET | `/api/roles/` | List all roles |
| GET | `/api/business-elements/` | List all elements |

### Mock Business Objects

**Products:**
- GET `/api/products/` - List products (filtered by permissions)
- POST `/api/products/` - Create product
- GET `/api/products/{id}/` - Get product
- PUT `/api/products/{id}/` - Update product
- DELETE `/api/products/{id}/` - Delete product

**Orders:**
- GET `/api/orders/` - List orders
- POST `/api/orders/` - Create order
- GET/PUT/DELETE `/api/orders/{id}/`

**Stores:**
- GET `/api/stores/` - List stores
- POST `/api/stores/` - Create store
- GET/PUT/DELETE `/api/stores/{id}/`

**Users:**
- GET `/api/users/` - List users (read-only)
- GET `/api/users/{id}/` - Get user

## 🔐 Permission System

### Permission Types

| Permission | Scope | Example |
|------------|-------|---------|
| read_permission | Own objects | User reads their products |
| read_all_permission | All objects | Admin reads all products |
| create_permission | New objects | User creates products |
| update_permission | Own objects | User updates their products |
| update_all_permission | All objects | Admin updates any product |
| delete_permission | Own objects | User deletes their products |
| delete_all_permission | All objects | Admin deletes any product |

### Permission Logic Flow

```

Request → Authenticate → Get User Roles → Query Access Rules
↓
Check Permission Type for Action
↓
Has *_all_permission? → YES → Grant Access
↓ NO
Has permission + owns object? → YES → Grant Access
↓ NO
Deny Access (403)

```

### Role Permissions Matrix

| Role | Products | Orders | Stores | Users | Access Rules |
|------|----------|--------|--------|-------|--------------|
| Admin | Full CRUD (all) | Full CRUD (all) | Full CRUD (all) | Full CRUD (all) | Full CRUD (all) |
| Manager | Full CRUD (all), no delete_all | Full CRUD (all) | CRUD (own) | Read (all) | No access |
| User | CRUD (own) | CRUD (own) | Read (all) | No access | No access |
| Guest | Read (all) | No access | Read (all) | No access | No access |

## 📝 Example Requests

### Register User
```

curl -X POST http://localhost:8000/api/auth/register/ \
-H "Content-Type: application/json" \
-d '{
"email": "john@example.com",
"first_name": "John",
"last_name": "Doe",
"password": "securepass123",
"password_confirmation": "securepass123"
}'

```

Response:
```json
{
    "message": "User registered successfully",
    "user_id": 7,
    "email": "john@example.com"
}
```

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{
    "email": "admin@test.com",
    "password": "password123"
}'
```

Response:
```json
{
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user_id": 1,
    "email": "admin@test.com",
    "first_name": "Admin",
    "last_name": "User"
}
```

### Get Profile
```bash
curl http://localhost:8000/api/auth/profile/ \
-H "Authorization: Bearer YOUR_TOKEN"
```

Response:
```json
{
    "id": 1,
    "email": "admin@test.com",
    "first_name": "Admin",
    "last_name": "User",
    "patronymic": "Administrator",
    "created_at": "2025-10-05T12:00:00Z",
    "updated_at": "2025-10-05T12:00:00Z"
}
```

### Create Product
```

curl -X POST http://localhost:8000/api/products/ \
-H "Authorization: Bearer YOUR_TOKEN" \
-H "Content-Type: application/json" \
-d '{
"name": "Laptop Pro",
"price": 1500,
"category": "Electronics"
}'

```

Response:
```

{
"id": 5,
"name": "Laptop Pro",
"price": 1500,
"category": "Electronics",
"owner_id": 1
}

```

### List Access Rules (Admin Only)
```

curl http://localhost:8000/api/access-rules/ \
-H "Authorization: Bearer ADMIN_TOKEN"

```

## 🚨 Error Responses

| Status Code | Meaning | Example |
|-------------|---------|---------|
| 400 | Bad Request | Invalid input data, validation errors |
| 401 | Unauthorized | Missing or invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource doesn't exist |
| 500 | Internal Server Error | Unexpected server error |

### Example Error Responses

**401 Unauthorized:**
```

{
"error": "Authentication required"
}

```

**403 Forbidden:**
```

{
"error": "Insufficient permissions"
}

```

**400 Bad Request:**
```

{
"email": ["This field is required."],
"password": ["Passwords do not match"]
}

```

## 🏗️ Project Structure

```
auth_system/
├── auth_system/              # Main project configuration
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # URL routing
│   ├── wsgi.py
│   └── asgi.py
├── authentication/           # Authentication app
│   ├── models.py            # User, Session models
│   ├── serializers.py       # DRF serializers
│   ├── views.py             # Auth endpoints
│   ├── urls.py              # Auth URL patterns
│   ├── middleware.py        # Custom auth middleware
│   ├── exceptions.py        # Custom exception handler
│   └── management/
│       └── commands/
│           └── seed_data.py # Database seeding
├── authorization/            # Authorization app
│   ├── models.py            # Role, AccessRule models
│   ├── serializers.py       # Authorization serializers
│   ├── views.py             # Admin API endpoints
│   ├── urls.py              # Authorization URLs
│   └── permissions.py       # Permission checker
├── mock_business/           # Mock business objects
│   ├── models.py            # (Minimal - using mock data)
│   ├── views.py             # CRUD endpoints
│   └── urls.py              # Business object URLs
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore rules
├── manage.py               # Django management
├── README.md               # This file
├── QUICKSTART.md           # Quick setup guide
├── SETUP_INSTRUCTIONS.md   # Detailed setup
├── DATABASE_SCHEMA.md      # Schema documentation
├── test_api.sh            # API test script
└── postman_collection.json # Postman collection
```

## 🛠️ Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| Django | 4.2.7 | Web framework |
| Django REST Framework | 3.14.0 | API framework |
| PostgreSQL | 15+ | Database |
| bcrypt | 4.1.1 | Password hashing |
| PyJWT | 2.8.0 | JWT token generation |
| psycopg2 | 2.9.9 | PostgreSQL adapter |
| python-decouple | 3.8 | Environment config |

## 🧪 Testing

### Manual Testing
```


# Run API test script

chmod +x test_api.sh
./test_api.sh

```

### Using Postman
1. Import `postman_collection.json`
2. Set base_url variable to `http://localhost:8000/api`
3. Run authentication requests first
4. Token is automatically saved for subsequent requests

### Using HTTPie
```


# Install httpie

brew install httpie  \# macOS

# or: pip install httpie

# Login

http POST localhost:8000/api/auth/login/ email=admin@test.com password=password123

# Use token

http GET localhost:8000/api/products/ Authorization:"Bearer TOKEN"

```

## 🔧 Development

### Database Management
```


# Create new migration

python manage.py makemigrations

# Apply migrations

python manage.py migrate

# Reseed database

python manage.py seed_data

# Access database shell

python manage.py dbshell

```

### Django Shell
```

python manage.py shell

# Example queries

>>> from authentication.models import User
>>> User.objects.all()
>>> User.objects.get(email='admin@test.com')

```

## 🚀 Production Deployment

### Before Deploying

1. **Update settings:**
   - Set `DEBUG=False`
   - Configure `ALLOWED_HOSTS`
   - Use strong `SECRET_KEY` and `JWT_SECRET`
   - Enable HTTPS

2. **Database:**
   - Use production database credentials
   - Enable connection pooling
   - Set up automated backups

3. **Server:**
   - Use Gunicorn or uWSGI
   - Configure Nginx as reverse proxy
   - Set up static file serving

4. **Security:**
   - Enable CSRF protection
   - Configure CORS headers
   - Set up rate limiting
   - Enable logging and monitoring

## 📊 Performance Considerations

- All foreign keys are indexed
- Email lookups are fast (unique index)
- Permission checks are optimized with composite indexes
- Query optimization for role-permission joins
- Recommended: Add Redis caching for permissions
- Recommended: Use connection pooling (pgBouncer)

## 🤝 Contributing

1. Add comprehensive unit tests
2. Implement API rate limiting
3. Add password reset functionality
4. Implement email verification
5. Add refresh token mechanism
6. Set up proper logging
7. Add API documentation (Swagger/OpenAPI)



## 📞 Support

For questions or issues during setup:
1. Check `SETUP_INSTRUCTIONS.md` for detailed steps
2. Review `DATABASE_SCHEMA.md` for schema details
3. Refer to `QUICKSTART.md` for quick reference

---

**Note:** This system demonstrates production-ready authentication and authorization patterns. All passwords are hashed with bcrypt, tokens expire after 24 hours, and the system follows security best practices throughout.
