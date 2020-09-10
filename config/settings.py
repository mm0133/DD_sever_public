import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from .my_settings import GOOGLE_OAUTH2_SECRET, NAVER_OAUTH2_SECRET, GITHUB_OAUTH2_SECRET

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "$c(@dpj2jqn7q+p8zi#qux_9^=nr+(!ms@6xr3_p)8goeu_4mq"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    # django default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # apps
    "api.users",
    "api.contests",
    "api.communications",
    "api.educations",
    "api.managements",

    # library
    "rest_framework",
    'social_django',  # django social auth
    'rest_social_auth',  # social login
    "corsheaders",
    'import_export',
    'dbbackup',  # django-dbbackup
    'django_extensions',
    'django_crontab',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"

# 파일 저장경로 관리
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')  # 개발자가 관리하는 파일들

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # 사용자가 업로드한 파일 관리

from . import my_settings

DATABASES = my_settings.DATABASES

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
    # 'DEFAULT_PERMISSION_CLASSES' : ('rest_framework.permissions.IsAuthenticated',),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend']
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = 'dataduck.ai@gmail.com'
EMAIL_HOST_PASSWORD = 'dataduckai20'

# authentication
SIMPLE_JWT = my_settings.SIMPLE_JWT

# social login
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'social_core.backends.naver.NaverOAuth2',
    'social_core.backends.github.GithubOAuth2',
    'social_core.backends.google.GoogleOAuth2',
)

SOCIAL_AUTH_PIPELINE =(
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.user.create_user',
    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details',
    'api.users.customPipeline.github_email'
)


# REST_SOCIAL_OAUTH_REDIRECT_URI = '/'
REST_SOCIAL_OAUTH_ABSOLUTE_REDIRECT_URI = 'http://127.0.0.1:3000/auth/social/callback'
REST_SOCIAL_DOMAIN_FROM_ORIGIN = False

SOCIAL_AUTH_GITHUB_KEY = '026f732d573c2afdead4'
SOCIAL_AUTH_GITHUB_SECRET = GITHUB_OAUTH2_SECRET
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']


SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = (
    '979510034981-hd4l7ldbj43c64q16q1dbpmcqa3r417e.apps.googleusercontent.com'
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = GOOGLE_OAUTH2_SECRET
SOCIAL_AUTH_GOOGLE_OAUTH2_SCOPE = ['email', ]

SOCIAL_AUTH_NAVER_KEY = 'aRXXE_H2v6yaj1bFX3eQ'
SOCIAL_AUTH_NAVER_SECRET = NAVER_OAUTH2_SECRET

DOMAIN_ADDRESS = ''
API_DOMAIN_ADDRESS = '/'

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True

DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': os.path.join(BASE_DIR, 'backup')}

CRONJOBS = [
    ('*/5 * * * *', 'contests.crons.give_medal_auto', '>> /log/medal_cron.log'),
]
