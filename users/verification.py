# users/verification.py

import datetime
import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


class EmailVerificationToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} - {self.token}"

    def is_valid(self):
        return timezone.now() < self.expires_at

    @classmethod
    def create_verification_token(cls, user):
        # Delete any existing tokens for this user
        cls.objects.filter(user=user).delete()

        # Create a new token
        token = uuid.uuid4().hex
        expires_at = timezone.now() + datetime.timedelta(days=2)  # Token valid for 2 days

        verification_token = cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )

        return verification_token

    def send_verification_email(self, request=None):
        """Send verification email to user"""
        # Use SITE_URL from settings if available, otherwise use request or fallback
        if hasattr(settings, 'SITE_URL') and settings.SITE_URL:
            domain = settings.SITE_URL.rstrip('/')
        elif request:
            domain = request.build_absolute_uri('/')[:-1]
        else:
            domain = 'https://agroconnectnaryn.org'

        # Generate new URL format (e.g., /
