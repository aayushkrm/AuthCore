from django.db import models
from django.utils import timezone
import bcrypt
import jwt
from datetime import datetime, timedelta
from django.conf import settings


class User(models.Model):
    """
    Custom User model without using Django's built-in authentication
    """
    email = models.EmailField(unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patronymic = models.CharField(max_length=100, blank=True, null=True)
    password_hash = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def set_password(self, raw_password):
        """Hash password using bcrypt"""
        salt = bcrypt.gensalt()
        self.password_hash = bcrypt.hashpw(
            raw_password.encode('utf-8'), 
            salt
        ).decode('utf-8')

    def check_password(self, raw_password):
        """Verify password against hash"""
        return bcrypt.checkpw(
            raw_password.encode('utf-8'),
            self.password_hash.encode('utf-8')
        )

    def generate_token(self):
        """Generate JWT token for user"""
        payload = {
            'user_id': self.id,
            'email': self.email,
            'exp': datetime.utcnow() + timedelta(hours=settings.JWT_EXPIRATION_HOURS),
            'iat': datetime.utcnow()
        }
        token = jwt.encode(
            payload, 
            settings.JWT_SECRET, 
            algorithm=settings.JWT_ALGORITHM
        )
        return token

    @staticmethod
    def decode_token(token):
        """Decode JWT token and return user_id"""
        try:
            payload = jwt.decode(
                token, 
                settings.JWT_SECRET, 
                algorithms=[settings.JWT_ALGORITHM]
            )
            return payload['user_id']
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

    def __str__(self):
        return self.email


class Session(models.Model):
    """
    Session model for session-based authentication (alternative to JWT)
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='sessions'
    )
    session_id = models.CharField(max_length=255, unique=True, db_index=True)
    expire_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sessions'
        ordering = ['-created_at']

    def is_valid(self):
        """Check if session is still valid"""
        return timezone.now() < self.expire_at

    @staticmethod
    def create_session(user, hours=24):
        """Create new session for user"""
        import secrets
        session_id = secrets.token_urlsafe(32)
        expire_at = timezone.now() + timedelta(hours=hours)
        return Session.objects.create(
            user=user,
            session_id=session_id,
            expire_at=expire_at
        )

    def __str__(self):
        return f"Session for {self.user.email}"
