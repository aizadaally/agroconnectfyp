# agroconnect_project/settings.py
# Add these imports at the top of settings.py
from django.utils.translation import gettext_lazy as _
import os
from pathlib import Path
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
from django.contrib.messages import constants as messages
import cloudinary
import cloudinary.uploader
import cloudinary.api


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


ALLOWED_HOSTS = ["*"]

# SITE_URL = 'https://agroconnectnaryn.org'

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cloudinary_storage',  # Add this
    'cloudinary',          # Add this
    
    # 'whitenoise.runserver_nostatic',


    
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'sslserver',
    
    # Custom apps
    'users',
    'products',
    'orders',
    'api',
    'frontend',
    'chatbot',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',  # SessionMiddleware must come first
    'django.middleware.locale.LocaleMiddleware',             # LocaleMiddleware must be here
    'corsheaders.middleware.CorsMiddleware',                 # Your CORS middleware
    'django.middleware.common.CommonMiddleware',             # Then CommonMiddleware
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Internationalization settings
# Set your language code to Kyrgyz as default
LANGUAGE_CODE = 'en'  # Default language (Kyrgyz)

# Define available languages
LANGUAGES = [
    ('en', _('English')),
    ('ru', _('Russian')),
    ('ky', _('Kyrgyz')),
]


# Location of translation files
USE_I18N = True
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

ROOT_URLCONF = 'agroconnect_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'frontend/templates')],  # Your existing setting
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'frontend.context_processors.language_context',  # Add this line
            ],
        },
    },
]

WSGI_APPLICATION = 'agroconnect_project.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv("ENGINE"),
        'NAME': os.getenv("PGNAME"),
        'USER': os.getenv("PGUSER"),
        'PASSWORD': os.getenv("PGPASSWORD"),
        'HOST': os.getenv("PGHOST"),
        'PORT': os.getenv("PGPORT"),
    }
}


# IO Intelligence API Configuration
# IO_INTELLIGENCE_API_KEY = os.getenv("IO_INTELLIGENCE_API_KEY", "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjMwNWE3OGU3LTA2ZTYtNGNjNS1hM2Q3LWQyMjdmMmU2MGI4YiIsImV4cCI6NDkwMDMxODYyN30.UJ_HrUC-EZhZcBEXCbl-1Ty80keYDa2mAjj8g61Q9nJnyM1xJlfy6Q4-QrYWZ9sDzROpz2AWDOse6ecnKtUifQ")

IO_INTELLIGENCE_API_KEY = "io-v2-eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJvd25lciI6IjMwNWE3OGU3LTA2ZTYtNGNjNS1hM2Q3LWQyMjdmMmU2MGI4YiIsImV4cCI6NDkwMDMxODYyN30.UJ_HrUC-EZhZcBEXCbl-1Ty80keYDa2mAjj8g61Q9nJnyM1xJlfy6Q4-QrYWZ9sDzROpz2AWDOse6ecnKtUifQ"
IO_INTELLIGENCE_ENDPOINT = "https://api.io.net/v1/chat/completions"
IO_INTELLIGENCE_MODEL = "llama-3-70b-chat"

# Email configuration
if DEBUG:
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
else:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    
    EMAIL_HOST = 'smtp.zoho.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")  # Zoho from email
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")  # Zoho App password
    DEFAULT_FROM_EMAIL = EMAIL_HOST_USER



# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Custom user model
AUTH_USER_MODEL = 'users.User'

# Internationalization
TIME_ZONE = 'UTC'
# USE_I18N = True  # Enable internationalization
USE_L10N = True  # Enable localization
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedStaticFilesStorage'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'static'),
]




# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Make sure this is after the MEDIA_URL and MEDIA_ROOT settings
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Cloudinary settings
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True,
    signature_algorithm='sha256'  # Add this line
)





# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS settings
CORS_ALLOW_ALL_ORIGINS = DEBUG  # In production, specify exact origins
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",
    
# ]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# Enable cookies in cross-site requests
CORS_ALLOW_CREDENTIALS = True


if not DEBUG:
    CSRF_TRUSTED_ORIGINS = ['https://agroconnect.up.railway.app', 'https://agroconnectnaryn.org']
    # SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
#     SECURE_HSTS_SECONDS = 31536000  # 1 year
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
    X_FRAME_OPTIONS = 'DENY'



# agroconnect_project/settings.py

# IO Intelligence API Configuration
# IO_INTELLIGENCE_API_KEY = os.getenv("IO_INTELLIGENCE_API_KEY")