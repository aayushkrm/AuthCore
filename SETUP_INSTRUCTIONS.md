## SETUP_INSTRUCTIONS.md

```markdown
# Complete Setup Instructions

Detailed step-by-step guide for setting up the Custom Authentication & Authorization System.

## 📖 Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Steps](#installation-steps)
- [Configuration](#configuration)
- [Database Setup](#database-setup)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)
- [Platform-Specific Notes](#platform-specific-notes)

## Prerequisites

### Required Software

| Software   | Minimum Version | Check Command       |
|------------|-----------------|---------------------|
| Python     | 3.8+            | `python3 --version` |
| PostgreSQL | 12+             | `psql --version`    |
| pip        | 20+             | `pip --version`     |

### Installation Guides

**Python:**
- macOS: `brew install python3`
- Linux: `sudo apt-get install python3 python3-pip`
- Windows: Download from [python.org](https://python.org)

**PostgreSQL:**
- macOS: `brew install postgresql@15`
- Linux: `sudo apt-get install postgresql postgresql-contrib`
- Windows: Download from [postgresql.org](https://postgresql.org)

## Installation Steps

### Step 1: Project Setup

```bash
# Navigate to project directory
cd /path/to/auth_system

# Verify project structure
ls -la

# Should see:
# - manage.py
# - requirements.txt
# - .env.example
# - README.md
# - auth_system/ directory
# - authentication/ directory
# - authorization/ directory
# - mock_business/ directory
```

### Step 2: Virtual Environment

**Why?** Isolates project dependencies from system Python.

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# macOS/Linux:
source venv/bin/activate

# Windows (Command Prompt):
venv\Scripts\activate.bat

# Windows (PowerShell):
venv\Scripts\Activate.ps1

# Verify activation (should see (venv) in prompt)
which python  # should show path inside venv/
```

### Step 3: Install Dependencies

```bash
# Upgrade pip (important!)
pip install --upgrade pip

# Install all requirements
pip install -r requirements.txt

# This installs:
# - Django 4.2.7
# - djangorestframework 3.14.0
# - psycopg2-binary 2.9.9 (PostgreSQL adapter)
# - bcrypt 4.1.1 (password hashing)
# - PyJWT 2.8.0 (JWT tokens)
# - python-decouple 3.8 (environment config)

# Verify installation
pip list
# Expected output includes all packages above
```

**Troubleshooting installations:**

```


# If psycopg2 fails on macOS:

brew install postgresql@15
echo 'export PATH="/usr/local/opt/postgresql@15/bin:\$PATH"' >> ~/.zshrc
source ~/.zshrc
pip install psycopg2-binary

# If bcrypt fails:

pip install --upgrade pip setuptools wheel
pip install bcrypt

```

## Configuration

### Step 1: Environment File

```


# Copy template

cp .env.example .env

# Verify copy

ls -la .env

```

### Step 2: Generate Secret Keys

**Django SECRET_KEY:**
```

python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

```

Copy output, example:
```

django-insecure-a8f\#$kd92@msdkf!29dkfj@#$kdf

```

**JWT SECRET_KEY:**
```

python3 -c "import secrets; print(secrets.token_urlsafe(50))"

```

Copy output, example:
```

xK7Hd9Pq2mR5nT8wY3vA6bZ1cF4gJ0sL9eN2oQ5pM7rU4iX8kV3hG6jB1tC0yW

```

### Step 3: Edit .env File

```


# Open with your preferred editor

nano .env

# or: vim .env

# or: code .env (VS Code)

```

**Configure all values:**

```


# Django Settings

SECRET_KEY=paste-your-django-secret-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# JWT Configuration

JWT_SECRET=paste-your-jwt-secret-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24

# Database Configuration

DB_ENGINE=django.db.backends.postgresql
DB_NAME=auth_system_db
DB_USER=your_database_username
DB_PASSWORD=your_database_password
DB_HOST=localhost
DB_PORT=5432

# Session Configuration

SESSION_EXPIRATION_HOURS=24

```

**Platform-Specific Database Config:**

**macOS:**
```

DB_USER=your_macos_username  \# check with: whoami
DB_PASSWORD=  \# leave empty if no password

```

**Linux:**
```

DB_USER=postgres  \# or your username
DB_PASSWORD=postgres  \# or your set password

```

**Windows:**
```

DB_USER=postgres
DB_PASSWORD=password  \# what you set during installation

```

Save and exit:
- nano: `Ctrl+X`, then `Y`, then `Enter`
- vim: `Esc`, then `:wq`, then `Enter`

## Database Setup

### Step 1: Start PostgreSQL

**macOS:**
```


# Check if running

brew services list | grep postgresql

# Start if not running

brew services start postgresql@15

# Verify

psql --version

```

**Linux:**
```


# Check status

sudo systemctl status postgresql

# Start if not running

sudo systemctl start postgresql

# Enable on boot

sudo systemctl enable postgresql

```

**Windows:**
```


# PostgreSQL should auto-start

# Check in Services app or:

sc query postgresql-x64-15

```

### Step 2: Create Database

**Method 1 - Using createdb (simplest):**
```

createdb auth_system_db

# Verify

psql -l | grep auth_system_db

```

**Method 2 - Using psql:**
```


# Connect to PostgreSQL

psql postgres

# Inside psql:

CREATE DATABASE auth_system_db;

# Verify

\l

# Expected output shows: auth_system_db

# Exit

\q

```

**Method 3 - Using pgAdmin (GUI):**
1. Open pgAdmin
2. Connect to your PostgreSQL server
3. Right-click "Databases"
4. Click "Create" → "Database"
5. Enter name: `auth_system_db`
6. Click "Save"

### Step 3: Verify Database Connection

```


# Test connection

psql -d auth_system_db -c "SELECT version();"

# Should show PostgreSQL version info

```

### Step 4: Run Migrations

```


# Create migration files

python manage.py makemigrations

# Expected output:

# Migrations for 'authentication':

# authentication/migrations/0001_initial.py

# - Create model User

# - Create model Session

# Migrations for 'authorization':

# authorization/migrations/0001_initial.py

# - Create model BusinessElement

# - Create model Role

# - Create model UserRole

# - Create model AccessRoleRule

# Apply migrations to database

python manage.py migrate

# Expected output:

# Operations to perform:

# Apply all migrations: authentication, authorization, contenttypes

# Running migrations:

# Applying authentication.0001_initial... OK

# Applying authorization.0001_initial... OK

# Applying contenttypes.0001_initial... OK

# Applying contenttypes.0002_remove_content_type_name... OK

```

### Step 5: Seed Test Data

```

python manage.py seed_data

```

**Expected output:**
```

Clearing existing data...
✓ Data cleared

Creating roles...
✓ Created role: admin
✓ Created role: manager
✓ Created role: user
✓ Created role: guest

Creating business elements...
✓ Created element: products
✓ Created element: users
✓ Created element: orders
✓ Created element: stores
✓ Created element: access_rules

Creating access rules...
✓ Created 5 rules for admin
✓ Created 4 rules for manager
✓ Created 3 rules for user
✓ Created 2 rules for guest

Creating test users...
✓ Created user: admin@test.com
✓ Created user: manager@test.com
✓ Created user: user1@test.com
✓ Created user: user2@test.com
✓ Created user: guest@test.com
✓ Created user: inactive@test.com (deactivated)

============================================================
DATABASE SEEDED SUCCESSFULLY!
============================================================

📊 Summary:

- Roles: 4
- Business Elements: 5
- Access Rules: 14
- Users: 6
- User-Role Assignments: 5

🔑 Test Accounts (all passwords: password123):

- admin@test.com      - Full system access
- manager@test.com    - Extended permissions
- user1@test.com      - Basic user access
- user2@test.com      - Basic user access
- guest@test.com      - Read-only access
- inactive@test.com   - Deactivated (cannot login)

============================================================

```

### Step 6: Verify Database

```


# Access Django shell

python manage.py shell

# Run verification commands:

>>> from authentication.models import User
>>> User.objects.count()
6

>>> from authorization.models import Role
>>> Role.objects.count()
4

>>> from authorization.models import AccessRoleRule
>>> AccessRoleRule.objects.count()
14

>>> exit()

```

## Testing

### Start Development Server

```

python manage.py runserver

# Expected output:

# Watching for file changes with StatReloader

# Performing system checks...

# System check identified no issues (0 silenced).

# October 05, 2025 - 19:00:00

# Django version 4.2.7, using settings 'auth_system.settings'

# Starting development server at http://127.0.0.1:8000/

# Quit the server with CONTROL-C.

```

**Server is running!** Keep this terminal open.

### Test API Endpoints

**Open a new terminal window:**

```


# Activate virtual environment in new terminal

cd /path/to/auth_system
source venv/bin/activate  \# or venv\Scripts\activate on Windows

```

**Test 1: Login**
```

curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "admin@test.com", "password": "password123"}'

```

**Expected response:**
```

{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"user_id": 1,
"email": "admin@test.com",
"first_name": "Admin",
"last_name": "User"
}

```

**Test 2: Get Profile (requires token)**
```


# Copy token from login response

TOKEN="paste_token_here"

curl http://localhost:8000/api/auth/profile/ \
-H "Authorization: Bearer $TOKEN"

```

**Expected response:**
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

**Test 3: List Products**
```

curl http://localhost:8000/api/products/ \
-H "Authorization: Bearer \$TOKEN"

```

**Expected response:**
```

[
{
"id": 1,
"name": "Laptop",
"price": 1200,
"category": "Electronics",
"owner_id": 1
},
{
"id": 2,
"name": "Mouse",
"price": 25,
"category": "Electronics",
"owner_id": 1
}
]

```

**Test 4: Create Product**
```

curl -X POST http://localhost:8000/api/products/ \
-H "Authorization: Bearer \$TOKEN" \
-H "Content-Type: application/json" \
-d '{"name": "Keyboard", "price": 75, "category": "Electronics"}'

```

**Expected response:**
```

{
"id": 5,
"name": "Keyboard",
"price": 75,
"category": "Electronics",
"owner_id": 1
}

```

**Test 5: Access Rules (Admin Only)**
```

curl http://localhost:8000/api/access-rules/ \
-H "Authorization: Bearer \$TOKEN"

```

**Expected response:** Array of access rules

**Test 6: Test Different User Roles**
```


# Login as regular user

curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "user1@test.com", "password": "password123"}'

# Save user1 token, then try to access admin endpoint

curl http://localhost:8000/api/access-rules/ \
-H "Authorization: Bearer USER1_TOKEN"

# Expected: 403 Forbidden

```

### Run Test Script

```


# Make executable

chmod +x test_api.sh

# Run all tests

./test_api.sh

```

This will test all endpoints automatically.

## Troubleshooting

### Common Issues

#### 1. "ModuleNotFoundError: No module named 'X'"

**Solution:**
```


# Ensure virtual environment is activated

source venv/bin/activate  \# macOS/Linux

# Reinstall requirements

pip install -r requirements.txt

```

#### 2. "connection to server ... failed: role 'postgres' does not exist"

**Solution:**
```


# Check your PostgreSQL username

whoami  \# macOS/Linux
echo %USERNAME%  \# Windows

# Update .env file:

DB_USER=your_actual_username
DB_PASSWORD=  \# leave empty if no password

```

#### 3. "createdb: command not found"

**macOS Solution:**
```


# Add PostgreSQL to PATH

echo 'export PATH="/usr/local/opt/postgresql@15/bin:\$PATH"' >> ~/.zshrc
source ~/.zshrc

# Verify

which createdb

```

**Linux Solution:**
```

sudo apt-get install postgresql-client

```

#### 4. "Port 8000 is already in use"

**Solution:**
```


# Run on different port

python manage.py runserver 8001

# Or kill existing process

lsof -ti:8000 | xargs kill -9  \# macOS/Linux

```

#### 5. "Authentication required" error

**Check:**
1. Token format: `Authorization: Bearer TOKEN` (note space after "Bearer")
2. Token is fresh (not expired - 24 hour expiry)
3. Token copied correctly without extra spaces
4. Header name is correct

**Test token manually:**
```


# Get fresh token

TOKEN=\$(curl -s -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "admin@test.com", "password": "password123"}' \
| grep -o '"token":"[^"]*' | cut -d'"' -f4)

echo \$TOKEN  \# Should print full token

# Use immediately

curl http://localhost:8000/api/products/ -H "Authorization: Bearer \$TOKEN"

```

#### 6. "CSRF verification failed"

**Solution:**
CSRF is disabled for API endpoints. If you see this error, check your Django settings:
```


# In settings.py, ensure:

REST_FRAMEWORK = {
'DEFAULT_AUTHENTICATION_CLASSES': [],
'DEFAULT_PERMISSION_CLASSES': [],
}

```

#### 7. Database migration errors

**Solution:**
```


# Delete migration files (except __init__.py)

rm authentication/migrations/0*.py
rm authorization/migrations/0*.py

# Recreate migrations

python manage.py makemigrations
python manage.py migrate

```

## Platform-Specific Notes

### macOS

**PostgreSQL Setup:**
```


# Install

brew install postgresql@15

# Add to PATH

echo 'export PATH="/usr/local/opt/postgresql@15/bin:\$PATH"' >> ~/.zshrc
source ~/.zshrc

# Start service

brew services start postgresql@15

# Database user is your macOS username

DB_USER=\$(whoami)

```

**Common macOS Issues:**
- Use `python3` not `python`
- Use `pip3` not `pip`
- PostgreSQL user = macOS username (no password by default)

### Linux (Ubuntu/Debian)

**PostgreSQL Setup:**
```


# Install

sudo apt-get update
sudo apt-get install postgresql postgresql-contrib

# Start service

sudo systemctl start postgresql
sudo systemctl enable postgresql

# Create user

sudo -u postgres createuser --interactive

# Name: your_username

# Superuser: yes

# Set password

sudo -u postgres psql
ALTER USER your_username WITH PASSWORD 'your_password';
\q

```

### Windows

**PostgreSQL Setup:**
1. Download installer from postgresql.org
2. Run installer
3. Remember the password you set for `postgres` user
4. Add to PATH if needed

**Virtual Environment:**
```


# Command Prompt

venv\Scripts\activate.bat

# PowerShell

venv\Scripts\Activate.ps1

```

**Path separators:** Use backslash `\` in Windows paths

## Verification Checklist

After completing setup, verify:

- [ ] ✅ Virtual environment activated (`(venv)` visible)
- [ ] ✅ All packages installed (`pip list` shows Django, DRF, etc.)
- [ ] ✅ `.env` file configured with all values
- [ ] ✅ PostgreSQL service running
- [ ] ✅ Database `auth_system_db` created
- [ ] ✅ Migrations applied successfully
- [ ] ✅ Test data seeded (6 users, 4 roles)
- [ ] ✅ Server starts without errors
- [ ] ✅ Can login and receive JWT token
- [ ] ✅ Protected endpoints require authentication (401 without token)
- [ ] ✅ Admin endpoints require admin role (403 for non-admin)
- [ ] ✅ Different users have different access levels

## Next Steps

After successful setup:

1. **Explore the API** - Test all endpoints with different users
2. **Review Code** - Understand the architecture
3. **Read Documentation** - Check README.md for API details
4. **Test Permissions** - Login as different roles
5. **Import Postman** - Use postman_collection.json for easier testing

## Development Workflow

```


# Daily workflow:

# 1. Activate environment

source venv/bin/activate

# 2. Start server

python manage.py runserver

# 3. Make changes to code

# 4. If models changed:

python manage.py makemigrations
python manage.py migrate

# 5. Test changes

./test_api.sh

# 6. Reseed if needed

python manage.py seed_data

```

## Getting Help

If you encounter issues:

1. Check this file for solutions
2. Review `QUICKSTART.md` for quick fixes
3. Check `DATABASE_SCHEMA.md` for schema details
4. Review `README.md` for API documentation

---

**Setup time:** 5-10 minutes (excluding PostgreSQL installation)

**Status:** If all verification checks pass, your system is ready for development and demonstration!
```

