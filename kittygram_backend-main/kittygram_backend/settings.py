import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY', 'CHANGE_ME_IN_PRODUCTION')

DEBUG = os.getenv('DEBUG', 'True').lower() in ('1', 'true', 'yes')  # По умолчанию True для разработки

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '*').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'whitenoise.runserver_nostatic',
	'corsheaders',
    'rest_framework.authtoken',
    'rest_framework',
    'djoser',
    'cats.apps.CatsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
	'whitenoise.middleware.WhiteNoiseMiddleware',
	'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'kittygram_backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend' / 'build'] if (BASE_DIR / 'frontend' / 'build').exists() else [],
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

WSGI_APPLICATION = 'kittygram_backend.wsgi.application'


DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.sqlite3',
		'NAME': BASE_DIR / 'db.sqlite3',
	}
}

# If DATABASE_URL is provided (e.g., on Railway), use it
DATABASE_URL = os.getenv('DATABASE_URL')
if DATABASE_URL:
	try:
		import dj_database_url  # type: ignore
		DATABASES['default'] = dj_database_url.parse(DATABASE_URL, conn_max_age=600)
	except Exception:
		# Fallback to default if parsing fails
		pass

# PostgreSQL configuration for Docker
if os.getenv('DB_ENGINE') == 'django.db.backends.postgresql':
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': os.getenv('DB_NAME', 'kittygram'),
			'USER': os.getenv('POSTGRES_USER', 'kittygram_user'),
			'PASSWORD': os.getenv('POSTGRES_PASSWORD', 'kittygram_password'),
			'HOST': os.getenv('DB_HOST', 'db'),
			'PORT': os.getenv('DB_PORT', '5432'),
		}
	}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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

USE_L10N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
# Enable compressed static files in production
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated', 
    ],

    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],

    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,

}

# Настройки Djoser для работы с пользователями
DJOSER = {
    'SERIALIZERS': {
        'user_create': 'djoser.serializers.UserCreateSerializer',
        'user': 'djoser.serializers.UserSerializer',
        'current_user': 'djoser.serializers.UserSerializer',
    },
    'PERMISSIONS': {
        'user': ['rest_framework.permissions.IsAuthenticated'],
        'user_list': ['rest_framework.permissions.AllowAny'],
        'user_create': ['rest_framework.permissions.AllowAny'],  # Разрешаем создание пользователей без аутентификации
    },
    'HIDE_USERS': False,  # Показывать пользователей
}

# CSRF trusted origins (add common Railway domain patterns by default)
default_csrf = ['https://*.up.railway.app', 'https://*.railway.app']
CSRF_TRUSTED_ORIGINS = os.getenv('CSRF_TRUSTED_ORIGINS', ','.join(default_csrf)).split(',')

# CORS settings
# Для разработки всегда разрешаем все источники
if DEBUG:
	CORS_ALLOW_ALL_ORIGINS = True
else:
	# В production используем настройки из переменных окружения
	if os.getenv('CORS_ALLOW_ALL_ORIGINS', 'false').lower() in ('1', 'true', 'yes'):
		CORS_ALLOW_ALL_ORIGINS = True
	else:
		CORS_ALLOWED_ORIGINS = [o for o in os.getenv('CORS_ALLOWED_ORIGINS', '').split(',') if o]

# Настройки для обслуживания React приложения
FRONTEND_DIR = BASE_DIR / 'frontend'
REACT_BUILD_DIR = FRONTEND_DIR / 'build'

# Добавляем папку build в STATICFILES_DIRS для production
if REACT_BUILD_DIR.exists():
	STATICFILES_DIRS = [
		REACT_BUILD_DIR / 'static',
	]