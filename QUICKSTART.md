

## QUICKSTART.md

```markdown
# Quick Start Guide

Get the Custom Authentication & Authorization System running in **5 minutes**.

## 📋 Prerequisites

- Python 3.8 or higher
- PostgreSQL 12 or higher
- Terminal/Command Line access

## 🚀 Setup Steps

### 1. Environment Setup

```


# Navigate to project directory

cd auth_system

# Create virtual environment

python3 -m venv venv

# Activate virtual environment

# macOS/Linux:

source venv/bin/activate

# Windows:

venv\Scripts\activate

# You should see (venv) in your prompt

```

### 2. Install Dependencies

```


# Upgrade pip

pip install --upgrade pip

# Install all requirements

pip install -r requirements.txt

# Verify installation

pip list

```

Expected output should include:
- Django==4.2.7
- djangorestframework==3.14.0
- psycopg2-binary==2.9.9
- bcrypt==4.1.1
- PyJWT==2.8.0
- python-decouple==3.8

### 3. Configure Environment Variables

```


# Copy template

cp .env.example .env

# Generate secret keys

python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Copy this output for SECRET_KEY

python3 -c "import secrets; print(secrets.token_urlsafe(50))"

# Copy this output for JWT_SECRET

# Edit .env file with your values

nano .env  \# or use your preferred editor

```

**Edit `.env` with:**
```

SECRET_KEY=paste-first-generated-key-here
JWT_SECRET=paste-second-generated-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=auth_system_db
DB_USER=your_username
DB_PASSWORD=your_password  \# leave empty if no password
DB_HOST=localhost
DB_PORT=5432

```

**Note for macOS/Linux:** Your database user is typically your system username. For macOS, use your macOS username (check with `whoami`).

### 4. Create PostgreSQL Database

**Option A - Using createdb (simplest):**
```

createdb auth_system_db

```

**Option B - Using psql:**
```

psql postgres

# Inside psql:

CREATE DATABASE auth_system_db;
\q

```

**Verify database:**
```

psql -l | grep auth_system_db

```

### 5. Initialize Database

```


# Create migration files

python manage.py makemigrations

# Apply migrations

python manage.py migrate

# Expected output:

# Applying authentication.0001_initial... OK

# Applying authorization.0001_initial... OK

# Applying contenttypes.0001_initial... OK

```

### 6. Load Test Data

```

python manage.py seed_data

```

Expected output:
```

✓ Data cleared
✓ Created role: admin
✓ Created role: manager
✓ Created role: user
✓ Created role: guest
✓ Created element: products
✓ Created element: users
✓ Created element: orders
✓ Created element: stores
✓ Created element: access_rules
✓ Created 5 rules for admin
✓ Created 4 rules for manager
✓ Created 3 rules for user
✓ Created 2 rules for guest
✓ Created user: admin@test.com
✓ Created user: manager@test.com
✓ Created user: user1@test.com
✓ Created user: user2@test.com
✓ Created user: guest@test.com
✓ Created user: inactive@test.com (deactivated)

DATABASE SEEDED SUCCESSFULLY!

```

### 7. Start Development Server

```

python manage.py runserver

```

Expected output:
```

Watching for file changes with StatReloader
Performing system checks...

System check identified no issues (0 silenced).
October 05, 2025 - 19:00:00
Django version 4.2.7, using settings 'auth_system.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.

```

✅ **Server is now running!**

## 🧪 Test the API

### Quick Test with curl

**Open a new terminal** and run:

```


# 1. Login as admin

curl -X POST http://localhost:8000/api/auth/login/ \
-H "Content-Type: application/json" \
-d '{"email": "admin@test.com", "password": "password123"}'

```

You should see:
```

{
"token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
"user_id": 1,
"email": "admin@test.com",
"first_name": "Admin",
"last_name": "User"
}

```

**2. Copy the token and test protected endpoint:**

```


# Replace YOUR_TOKEN with the actual token from above

TOKEN="your_token_here"

curl http://localhost:8000/api/auth/profile/ \
-H "Authorization: Bearer \$TOKEN"

```

**3. List products:**
```

curl http://localhost:8000/api/products/ \
-H "Authorization: Bearer \$TOKEN"

```

**4. Create a product:**
```

curl -X POST http://localhost:8000/api/products/ \
-H "Authorization: Bearer \$TOKEN" \
-H "Content-Type: application/json" \
-d '{"name": "Laptop", "price": 1200, "category": "Electronics"}'

```

## 🔑 Test Accounts

All passwords: `password123`

| Email | Role | Description |
|-------|------|-------------|
| admin@test.com | Admin | Full system access |
| manager@test.com | Manager | Extended permissions |
| user1@test.com | User | Basic access (own data only) |
| user2@test.com | User | Basic access (own data only) |
| guest@test.com | Guest | Read-only access |

## 🎯 Key Endpoints to Test

### Authentication
```


# Register

POST /api/auth/register/

# Login

POST /api/auth/login/

# Get profile

GET /api/auth/profile/

# Update profile

PUT /api/auth/profile/

# Logout

POST /api/auth/logout/

```

### Business Objects
```


# Products

GET /api/products/
POST /api/products/
GET /api/products/1/
PUT /api/products/1/
DELETE /api/products/1/

# Orders

GET /api/orders/

# Stores

GET /api/stores/

# Users (read-only)

GET /api/users/

```

### Admin Only
```


# Access rules

GET /api/access-rules/
POST /api/access-rules/
GET /api/access-rules/1/
PUT /api/access-rules/1/
DELETE /api/access-rules/1/

# Roles

GET /api/roles/

# Business elements

GET /api/business-elements/

```

## 🛠️ Common Commands

```


# Reseed database (if needed)

python manage.py seed_data

# Check migrations status

python manage.py showmigrations

# Access Django shell

python manage.py shell

# Access database shell

python manage.py dbshell

# View routes

python manage.py show_urls  \# if django-extensions installed

```

## ⚠️ Troubleshooting

### Issue: "command not found: createdb"

**macOS:**
```


# Add PostgreSQL to PATH

echo 'export PATH="/usr/local/opt/postgresql@15/bin:\$PATH"' >> ~/.zshrc
source ~/.zshrc

```

**Solution:** Install PostgreSQL first:
```


# macOS

brew install postgresql@15
brew services start postgresql@15

# Linux (Ubuntu/Debian)

sudo apt-get install postgresql postgresql-contrib
sudo systemctl start postgresql

```

### Issue: "role 'postgres' does not exist"

**Fix:** Use your system username in `.env`:
```


# macOS/Linux - use your username (check with: whoami)

DB_USER=your_username
DB_PASSWORD=  \# leave empty if no password set

```

### Issue: "Authentication required" error

**Check:**
1. Token format: `Authorization: Bearer TOKEN`
2. Token is fresh (not expired)
3. Token copied correctly (no extra spaces)

### Issue: Port 8000 already in use

```


# Run on different port

python manage.py runserver 8001

# Or kill existing process

# macOS/Linux:

lsof -ti:8000 | xargs kill -9

# Windows:

netstat -ano | findstr :8000
taskkill /PID <PID> /F

```

### Issue: "No module named 'decouple'"

```


# Make sure virtual environment is activated

source venv/bin/activate  \# macOS/Linux

# venv\Scripts\activate   \# Windows

# Reinstall requirements

pip install -r requirements.txt

```

### Issue: Database connection error

```


# Check PostgreSQL is running

# macOS:

brew services list

# Linux:

sudo systemctl status postgresql

# Start if not running:

brew services start postgresql@15  \# macOS
sudo systemctl start postgresql    \# Linux

```

## ✅ Verification Checklist

After setup, verify:
- [ ] Virtual environment activated (see `(venv)` in prompt)
- [ ] All dependencies installed (`pip list` shows Django, DRF, etc.)
- [ ] Database created (`psql -l` shows auth_system_db)
- [ ] Migrations applied (no pending migrations)
- [ ] Test data seeded (6 users created message)
- [ ] Server starts without errors
- [ ] Can login and receive JWT token
- [ ] Protected endpoints require authentication
- [ ] Different roles have different access levels

## 🎉 Success!

If you've completed all steps and verified the checklist, your system is **fully operational**!

## 📚 Next Steps

1. **Explore the API** - Try different endpoints with different user roles
2. **Read documentation** - Check `README.md` for detailed API docs
3. **Review schema** - See `DATABASE_SCHEMA.md` for database design
4. **Test permissions** - Login as different users to see permission differences
5. **Import Postman collection** - Use `postman_collection.json` for easier testing

## 🆘 Need Help?

- **Detailed setup:** See `SETUP_INSTRUCTIONS.md`
- **Database schema:** See `DATABASE_SCHEMA.md`
- **API documentation:** See `README.md`
- **Test script:** Run `./test_api.sh` for automated tests

---

**Estimated setup time:** 3-5 minutes (excluding PostgreSQL installation)

**Questions?** All test credentials are `password123` for easy testing.