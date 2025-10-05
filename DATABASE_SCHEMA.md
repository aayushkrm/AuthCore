# Database Schema Documentation

Complete database schema documentation for the Custom Authentication & Authorization System.

## Overview

The system uses **PostgreSQL** and consists of 6 main tables implementing custom authentication and role-based access control (RBAC).

## Entity Relationship Diagram (ERD)

```ascii
┌──────────────┐
│     users    │
└──────────────┘
         │
         │ 1
         │
         │ *
┌──────────────┐
│  user_roles  │
└──────────────┘
         │
         │ *
         │
         │ 1
┌──────────────┐         ┌───────────────────┐
│    roles     │─────────│ access_roles_rules │
└──────────────┘         └───────────────────┘
         │
         │ *
         │
         │ 1
┌──────────────┐
│business_elem.│
└──────────────┘

┌──────────────┐
│   sessions   │
│  (optional)  │
└──────────────┘
         │ *
         │
         │ 1
┌──────────────┐
│     users    │
└──────────────┘
```

## Table Details

### 1. users

**Description:** Stores user account information and authentication credentials.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique user identifier |
| email | VARCHAR(254) | UNIQUE, NOT NULL, INDEXED | User's email address (login) |
| first_name | VARCHAR(100) | NOT NULL | User's first name |
| last_name | VARCHAR(100) | NOT NULL | User's last name |
| patronymic | VARCHAR(100) | NULL | User's patronymic/middle name |
| password_hash | VARCHAR(255) | NOT NULL | Bcrypt hashed password |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Account status (for soft delete) |
| created_at | TIMESTAMP | NOT NULL, AUTO | Account creation timestamp |
| updated_at | TIMESTAMP | NOT NULL, AUTO | Last update timestamp |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `email`

**Notes:**
- Passwords are hashed using bcrypt with salt
- `is_active=False` implements soft delete
- Email is used as username for authentication

---

### 2. roles

**Description:** Defines available roles in the system.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique role identifier |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Role name (admin, manager, user, guest) |
| description | TEXT | NULL | Role description |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `name`

**Default Roles:**
- **admin** - Full system access
- **manager** - Extended permissions
- **user** - Basic user permissions
- **guest** - Read-only access

---

### 3. user_roles

**Description:** Junction table for many-to-many relationship between users and roles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique identifier |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | Reference to user |
| role_id | INTEGER | FOREIGN KEY → roles.id, NOT NULL | Reference to role |
| assigned_at | TIMESTAMP | NOT NULL, AUTO | Role assignment timestamp |

**Constraints:**
- UNIQUE (user_id, role_id) - User can have each role only once
- ON DELETE CASCADE - Delete assignment if user or role deleted

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `user_id`
- INDEX on `role_id`
- UNIQUE INDEX on (user_id, role_id)

**Notes:**
- A user can have multiple roles
- A role can be assigned to multiple users

---

### 4. business_elements

**Description:** Defines business resources/entities that can be protected by access control.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique element identifier |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Element name (products, orders, etc.) |
| description | TEXT | NULL | Element description |

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `name`

**Default Elements:**
- **products** - Product catalog
- **users** - User management
- **orders** - Order management
- **stores** - Store locations
- **access_rules** - Access control rules

---

### 5. access_roles_rules

**Description:** Defines granular permissions for each role on each business element.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique rule identifier |
| role_id | INTEGER | FOREIGN KEY → roles.id, NOT NULL | Reference to role |
| element_id | INTEGER | FOREIGN KEY → business_elements.id, NOT NULL | Reference to business element |
| read_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can read own objects |
| read_all_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can read all objects |
| create_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can create new objects |
| update_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can update own objects |
| update_all_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can update all objects |
| delete_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can delete own objects |
| delete_all_permission | BOOLEAN | NOT NULL, DEFAULT FALSE | Can delete all objects |

**Constraints:**
- UNIQUE (role_id, element_id) - One rule per role per element
- ON DELETE CASCADE - Delete rule if role or element deleted

**Indexes:**
- PRIMARY KEY on `id`
- INDEX on `role_id`
- INDEX on `element_id`
- UNIQUE INDEX on (role_id, element_id)

**Permission Hierarchy:**

```

*_all_permission > regular_permission

```

**Permission Logic:**
- If `*_all_permission` is TRUE → Access granted to ALL objects
- If regular permission is TRUE → Check ownership (owner_id == user.id)
- If both FALSE → Access denied

---

### 6. sessions

**Description:** Optional table for session-based authentication (alternative to JWT).

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | SERIAL | PRIMARY KEY | Unique session identifier |
| user_id | INTEGER | FOREIGN KEY → users.id, NOT NULL | Reference to user |
| session_id | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | Session token |
| expire_at | TIMESTAMP | NOT NULL | Session expiration time |
| created_at | TIMESTAMP | NOT NULL, AUTO | Session creation time |

**Constraints:**
- ON DELETE CASCADE - Delete session if user deleted

**Indexes:**
- PRIMARY KEY on `id`
- UNIQUE INDEX on `session_id`
- INDEX on `user_id`

**Notes:**
- Used only if implementing session-based auth instead of JWT
- Sessions are automatically cleaned up on logout
- Expired sessions should be periodically purged

---

## Permission Matrix Example

Example access rules for different roles on the 'products' element:

| Role | read | read_all | create | update | update_all | delete | delete_all |
|------|------|----------|--------|--------|------------|--------|------------|
| admin | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ✅ |
| manager | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ | ❌ |
| user | ✅ | ❌ | ✅ | ✅ | ❌ | ✅ | ❌ |
| guest | ❌ | ✅ | ❌ | ❌ | ❌ | ❌ | ❌ |

**Legend:**
- ✅ = Permission granted
- ❌ = Permission not granted

**Interpretation:**
- **admin**: Can see all products, create, update any, delete any
- **manager**: Can see all products, create, update any, but cannot delete
- **user**: Can only see/manage their own products (full CRUD on owned)
- **guest**: Can only view all products (read-only)

---

## SQL Schema

### Create Tables SQL

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(254) UNIQUE NOT NULL,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    patronymic VARCHAR(100),
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT TRUE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_is_active ON users(is_active);

-- Roles table
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

-- User roles junction table
CREATE TABLE user_roles (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    assigned_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, role_id)
);

CREATE INDEX idx_user_roles_user ON user_roles(user_id);
CREATE INDEX idx_user_roles_role ON user_roles(role_id);

-- Business elements table
CREATE TABLE business_elements (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

-- Access rules table
CREATE TABLE access_roles_rules (
    id SERIAL PRIMARY KEY,
    role_id INTEGER NOT NULL REFERENCES roles(id) ON DELETE CASCADE,
    element_id INTEGER NOT NULL REFERENCES business_elements(id) ON DELETE CASCADE,
    read_permission BOOLEAN NOT NULL DEFAULT FALSE,
    read_all_permission BOOLEAN NOT NULL DEFAULT FALSE,
    create_permission BOOLEAN NOT NULL DEFAULT FALSE,
    update_permission BOOLEAN NOT NULL DEFAULT FALSE,
    update_all_permission BOOLEAN NOT NULL DEFAULT FALSE,
    delete_permission BOOLEAN NOT NULL DEFAULT FALSE,
    delete_all_permission BOOLEAN NOT NULL DEFAULT FALSE,
    UNIQUE(role_id, element_id)
);

CREATE INDEX idx_access_rules_role ON access_roles_rules(role_id);
CREATE INDEX idx_access_rules_element ON access_roles_rules(element_id);

-- Sessions table (optional)
CREATE TABLE sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(255) UNIQUE NOT NULL,
    expire_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_sessions_user ON sessions(user_id);
CREATE INDEX idx_sessions_session_id ON sessions(session_id);
```

---

## Querying Examples

### Get all roles for a user
```sql
SELECT r.name, r.description
FROM roles r
    JOIN user_roles ur ON r.id = ur.role_id
WHERE ur.user_id = 1;
```

### Get all permissions for a role on a specific element
```sql
SELECT
    r.name as role_name,
    be.name as element_name,
    arr.*
FROM access_roles_rules arr
    JOIN roles r ON arr.role_id = r.id
    JOIN business_elements be ON arr.element_id = be.id
WHERE r.name = 'user' 
    AND be.name = 'products';
```

### Check if user has specific permission
```sql
SELECT EXISTS (
    SELECT 1
    FROM access_roles_rules arr
        JOIN user_roles ur ON arr.role_id = ur.role_id
        JOIN business_elements be ON arr.element_id = be.id
    WHERE ur.user_id = 1
        AND be.name = 'products'
        AND arr.create_permission = TRUE
) as has_permission;
```

### Get all active users with their roles
```sql
SELECT
    u.email,
    u.first_name,
    u.last_name,
    STRING_AGG(r.name, ', ') as roles
FROM users u
    LEFT JOIN user_roles ur ON u.id = ur.user_id
    LEFT JOIN roles r ON ur.role_id = r.id
WHERE u.is_active = TRUE
GROUP BY u.id, u.email, u.first_name, u.last_name;
```

---

## Data Integrity Rules

1. **User Email Uniqueness**: Each email can only be registered once
2. **Role Assignment Uniqueness**: User cannot have the same role twice
3. **Access Rule Uniqueness**: One rule per role per element
4. **Cascade Deletes**: Deleting a user removes their roles and sessions
5. **Active Status**: Soft delete preserves data integrity
6. **Timestamp Tracking**: All entities track creation time

---

## Performance Considerations

### Indexes
- All foreign keys are indexed
- Unique constraints create indexes automatically
- Email lookups are fast (indexed)
- Permission checks are optimized with composite indexes

### Query Optimization
- Use JOIN instead of multiple queries
- Cache user roles in application layer
- Index on `is_active` for user queries
- Composite index on (role_id, element_id) for permission checks

### Scaling Recommendations
- Add read replicas for heavy read workloads
- Implement Redis caching for permissions
- Consider partitioning if user table > 10M rows
- Use connection pooling (pgBouncer)

---

## Backup and Maintenance

### Backup Strategy
```bash
# Full database backup
pg_dump -U postgres auth_system_db > backup_$(date +%Y%m%d).sql

# Restore from backup
psql -U postgres auth_system_db < backup_20251005.sql
```

### Maintenance Tasks
```sql
-- Clean expired sessions (if using session-based auth)
DELETE FROM sessions WHERE expire_at < NOW();

-- Vacuum analyze for performance
VACUUM ANALYZE users;
VACUUM ANALYZE access_roles_rules;
```

---

## Migration History

When you run migrations, Django tracks them in the `django_migrations` table:

```

SELECT * FROM django_migrations ORDER BY applied DESC;

```

This helps track schema changes over time.

---

## Additional Notes

- All timestamps are stored in UTC
- Boolean fields default to FALSE for security (deny by default)
- Soft delete (is_active) maintains referential integrity
- Password hashes are 60 characters (bcrypt standard)
- Session IDs are URL-safe base64 encoded (43 characters)

