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
    ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1,10.0.2.2,10.161.1.211', cast=lambda v: [s.strip() for s in v.split(',')])
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
    'whitenoise.middleware.WhiteNoiseMiddleware',
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
# Use PostgreSQL on Render, SQLite locally, MongoDB optional for additional data
is_render = os.environ.get('RENDER') == 'true'

if is_render:
    # Render deployment - use PostgreSQL database
    # Render automatically provides these environment variables for PostgreSQL:
    # DATABASE_URL=postgresql://user:pass@host:port/dbname
    try:
        import dj_database_url
        DATABASE_URL = config(
            'DATABASE_URL',
            default='postgresql://blueprint_postures_learn_user:FOlENaCbVYqr9ZwBOE5QEkSRxkKgp8Lv@dpg-d3s34rodl3ps73d29o70-a:5432/blueprint_postures_learn'
        )
        # Use dj_database_url to parse connection string
        DATABASES = {
            'default': dj_database_url.config(
                default=DATABASE_URL,
                conn_max_age=600,
                conn_health_checks=True,
            )
        }
        print("🐘 Using PostgreSQL on Render")
    except Exception as e:
        # Fallback configuration
        DATABASE_URL = config(
            'DATABASE_URL',
            default='postgresql://blueprint_postures_learn_user:FOlENaCbVYqr9ZwBOE5QEkSRxkKgp8Lv@dpg-d3s34rodl3ps73d29o70-a:5432/blueprint_postures_learn'
        )
        # Manual fallback configuration
        from urllib.parse import urlparse
        db_url = urlparse(DATABASE_URL)
        DATABASES = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql',
                'NAME': db_url.path[1:] if db_url.path.startswith('/') else db_url.path,
                'USER': db_url.username or '',
                'PASSWORD': db_url.password or '',
                'HOST': db_url.hostname or '',
                'PORT': db_url.port or 5432,
            }
        }
        print(f"🐘 Using PostgreSQL on Render (fallback): {str(e)[:50]}")
else:
    # Local development - use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
    print("🏠 Local development - using SQLite")

# MongoDB Atlas configuration for additional data storage
# Priority: environment variable > .env file > default Atlas URI
MONGODB_URI = config('MONGODB_URI', default='mongodb+srv://adminN:nSkTkOFijiEWfdsoksd@cluster0.bn7mgbx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
MONGODB_DATABASE = config('MONGODB_DATABASE', default='hackwesttx_db')
MONGODB_ENABLED = config('MONGODB_ENABLED', default=True, cast=bool)
MONGODB_TIMEOUT = config('MONGODB_TIMEOUT', default=10, cast=int)  # Connection timeout in seconds

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
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Use Django's default User model
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
CORS_ALLOWED_ORIGINS = config('CORS_ALLOWED_ORIGINS', default='http://localhost:3000,http://localhost:5173,http://10.0.2.2:8000,http://10.161.1.211:8000', cast=lambda v: [s.strip() for s in v.split(',')])
CORS_ALLOW_CREDENTIALS = True

# Allow all origins for development (remove in production)
CORS_ALLOW_ALL_ORIGINS = True

# OpenAI API Key for file processing and summarization
OPENAI_API_KEY = config('OPENAI_API_KEY', default='')
