from pathlib import Path
import os
import environ
from datetime import timedelta
from django.core.exceptions import ImproperlyConfigured

root = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = env.str('SECRET_KEY', "rcmgihae;gmh'weaor3149")

DEBUG = env.bool('DEBUG', default=True)

ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://hack-solution.tech']

INSTALLED_APPS = [
    'graphene_django',

    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',

    'taggit',
    'modelcluster',

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'drf_spectacular',
    'drf_spectacular_sidecar',
    'storages',
    'mozilla_django_oidc',

    'Authentication.apps.AuthenticationConfig',
    'Company.apps.CompanyConfig',
    'Test.apps.TestConfig',
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

    'mozilla_django_oidc.middleware.SessionRefresh',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["./"],
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

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {}

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': env.str('DATABASE_NAME'),
            'USER': env.str('DATABASE_USER'),
            'PASSWORD': env.str('DATABASE_PASSWORD'),
            'HOST': env.str('DATABASE_HOST'),
            'PORT': env.str('DATABASE_PORT'),
        }
    }

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

public_root = root.path('public/')
MEDIA_ROOT = 'media'
MEDIA_URL = env.str('MEDIA_URL', default='media/')
STATIC_ROOT = 'static'
STATIC_URL = env.str('STATIC_URL', default='static/')

if not DEBUG:
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'

    AWS_ACCESS_KEY_ID = os.getenv('MINIO_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('MINIO_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('MINIO_STORAGE_BUCKET_NAME')
    AWS_S3_ENDPOINT_URL = os.getenv('MINIO_API')
    AWS_S3_USE_SSL = False


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'Authentication.CustomUser'


REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(days=2),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}


CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

WAGTAIL_SITE_NAME = 'LDT'

GRAPHENE = {
    "SCHEMA": "Company.schema.schema",
}

AUTHENTICATION_BACKENDS = (
    'project.auth.KeycloakOIDCAuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',
)

OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")

OIDC_DOMAIN = env.str("OIDC_DOMAIN", '')
OIDC_REALM = env.str("OIDC_REALM", '')

OIDC_RP_SIGN_ALGO = 'RS256'

OIDC_USERNAME_GENERATOR = 'project.auth.generate_username'

OIDC_AUTH_URI = f"http://{OIDC_DOMAIN}/realms/{OIDC_REALM}"
OIDC_OP_AUTHORIZATION_ENDPOINT = f'{OIDC_AUTH_URI}/protocol/openid-connect/auth'
OIDC_OP_TOKEN_ENDPOINT = f'{OIDC_AUTH_URI}/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = f'{OIDC_AUTH_URI}/protocol/openid-connect/userinfo'
OIDC_OP_JWKS_ENDPOINT = f'{OIDC_AUTH_URI}/protocol/openid-connect/certs'
OIDC_TOKEN_USE_BASIC_AUTH = True
OIDC_USER_MODEL = 'Authentication.CustomUser'

LOGIN_URL = '/oidc/authenticate/'

SPECTACULAR_SETTINGS = {
    'TITLE': 'TLD',
    'DESCRIPTION': '',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
    'COMPONENT_SPLIT_REQUEST': True,
}
