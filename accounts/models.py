from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Role(models.TextChoices):
    COMPANY = 'COMPANY', 'Company'
    CENTER = 'CENTER', 'Center'
    ADMIN = 'ADMIN', 'Admin'
    STUDENT = 'STUDENT', 'Student'


class AppUser(models.Model):
    """Unified user model - one account, role-based access."""
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=50, blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.COMPANY)
    # Link to legacy models (IDs stored for session)
    company_id = models.PositiveIntegerField(null=True, blank=True)
    center_id = models.PositiveIntegerField(null=True, blank=True)
    admin_id = models.PositiveIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.email} ({self.role})"
