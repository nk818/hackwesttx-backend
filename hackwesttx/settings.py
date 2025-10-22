from decouple import config
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

DEBUG = config('DEBUG', default=True, cast=bool)

# ALLOWED_HOSTS configuration for Railway deployment
import os

# Check if we're on Railway (multiple ways to detect)
is_railway = (
    os.environ.get('RAILWAY_ENVIRONMENT') or 
    os.environ.get('RAILWAY_PROJECT_ID') or 
    os.environ.get('PORT')  # Railway always sets PORT
)

if is_railway:
    # Railway deployment - allow all domains
    ALLOWED_HOSTS = ['*']
    print("🚀 Railway deployment detected - ALLOWED_HOSTS set to ['*']")
else:
    # Local development
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,10.0.2.2', cast=lambda v: [s.strip() for s in v.split(',')])
    print("🏠 Local development - using specific ALLOWED_HOSTS")

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'api',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'hackwesttx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hackwesttx.wsgi.application'

# Database configuration
# Use PostgreSQL on Render, SQLite locally
is_render = os.environ.get('RENDER') == 'true'

if is_render:
    # Render deployment - use PostgreSQL
    # Try to use DATABASE_URL first, then fall back to individual variables
    database_url = os.environ.get('DATABASE_URL')
    if database_url:
        import dj_database_url
        DATABASES = {
            'default': dj_database_url.parse(database_url)
        }
        print("🚀 Render deployment - using DATABASE_URL")
    else:
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': os.environ.get('DB_NAME', 'railway'),
                'USER': os.environ.get('DB_USER', 'postgres'),
                'PASSWORD': os.environ.get('DB_PASSWORD', ''),
                'HOST': os.environ.get('DB_HOST', 'localhost'),
                'PORT': os.environ.get('DB_PORT', '5432'),
            }
        }
        print("🚀 Render deployment - using individual database variables")
elif is_railway:
    # Railway deployment - use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': '/tmp/db.sqlite3',
        }
    }
    print("🚀 Railway deployment - using SQLite database at /tmp/db.sqlite3")
else:
    # Local development - use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("🏠 Local development - using SQLite database")

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

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'api.User'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
}

# CORS settings
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://localhost:5173,http://10.0.2.2:8000', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOW_CREDENTIALS = True

# Allow all origins for development (remove in production)
CORS_ALLOW_ALL_ORIGINS = True

# OpenAI API Key for file processing and summarization
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')

# MongoDB Configuration
MONGODB_URI = config('MONGODB_URI', default='mongodb+srv://noahkueng1_db_user:tc2FviW6Wa5kxjEO@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')

# MongoDB Connection Settings
MONGODB_ENABLED = config('MONGODB_ENABLED', default=False, cast=bool)
MONGODB_TIMEOUT = 5  # 5 second timeout for MongoDB connections
