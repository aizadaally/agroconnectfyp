# Create this as users/migrations/0003_user_email_verified.py

from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_bank_account_user_bank_name_user_bank_qr_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='email_verified',
            field=models.BooleanField(default=False),
        ),
    ]