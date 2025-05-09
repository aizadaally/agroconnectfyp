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

        # Generate the verification URL
        # Include language code in URL for internationalization
        lang_code = getattr(request, 'LANGUAGE_CODE', 'en')
        verification_url = f"{domain}/{lang_code}/verify-email/{self.token}/"
        
        # Format the email with a proper template
        context = {
            'user': self.user,
            'verification_url': verification_url,
            'expiry_time': self.expires_at.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        # Render the HTML email template
        html_message = render_to_string('emails/verify_email.html', context)
        plain_message = strip_tags(html_message)
        
        # Send the email
        try:
            result = send_mail(
                subject='Verify Your Email - AgroConnect Naryn',
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.user.email],
                html_message=html_message,
                fail_silently=False,
            )
            print(f"Verification email send result: {result} to {self.user.email}")
            return True
        except Exception as e:
            print(f"Error sending verification email: {str(e)}")
            import traceback
            traceback.print_exc()
            return False