import os
import raven


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'zbua(=8tqz9(l_wkqapp!j4@c2&qnkgtk+=4-30f+td(_gr_2w'

DEBUG = False

ALLOWED_HOSTS = [
    'www.tratum.co', 
    'tratum.co', 
    '206.81.10.147'
]

API_KEY = 'b7b15cc877c0c0c2d8e6aeee4e68296df24656a2'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'django.contrib.humanize',
    'rest_framework',
    'rest_framework.authtoken',
    'rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'rest_auth.registration',
    'import_export',
    'mptt_urls',
    'embed_video',
    'raven.contrib.django.raven_compat',
    'smart_selects',
    'api',
    'ckeditor',
    'mptt',
    'utils',
    'document_manager',
    'business_info',
    'store',
    'users',
    'webclient',
    'reports'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'tratum.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'tratum/templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'webclient.context_processors.categories.context_categories',
                'webclient.context_processors.api-key.api_key_processor',
                'webclient.context_processors.faq.faq_processor',
                'webclient.context_processors.bussiness_info.bussiness_info_processor',
            ],
        },
    },
]

WSGI_APPLICATION = 'tratum.wsgi.application'

SITE_ID = 1


# Database

DATABASES = {
    'default': {
        'NAME': 'tratum',
        'USER': 'tratum',
        'PASSWORD': 'plJhgdCuyKnuyVasfmbtcg',
        'ENGINE': 'django.db.backends.postgresql'
    }
}


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


# Internationalization

LANGUAGE_CODE = 'es-CO'

TIME_ZONE = 'America/Bogota'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static and files 

STATIC_URL = '/static/'
STATIC_ROOT = "/var/www/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tratum/static"),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = "/var/www/media/"

# CKEditor config

CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'moono',
        'toolbar_CustomToolbarConfig': [
            {
                'name': 'document',
                'items': [
                    'Save'
                ]
            },
            {
                'name': 'clipboard',
                'items': [
                    'Cut',
                    'Copy',
                    'Paste',
                    '-',
                    'Undo',
                    'Redo'
                ]
            },
            {
                'name': 'basicstyles',
                'items': [
                    'Bold',
                    'Italic',
                    'Underline'
                ]
            },
            {
                'name': 'paragraph',
                'items': [
                    'JustifyLeft',
                    'JustifyCenter',
                    'JustifyRight',
                    'JustifyBlock'
                ]
            },
            {
                'items': [
                    'Maximize',
                ]
            },
            {
                'name': 'documentfield',
                'items': ['documentfield']
            },
            {
                'name': 'documentsection',
                'items': ['documentsection']
            },
            {
                'name': 'dynamiccounter',
                'items': ['dynamiccounter']
            },
            {
                'name': 'conditional',
                'items': ['conditional']
            }
        ],
        'toolbar': 'CustomToolbarConfig', 
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'ajax',
            'autolink',
            'autoembed',
            'embedsemantic',
            'autogrow',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath',
            'documentfield',
            'documentsection',
            'dynamiccounter',
            'conditional'
        ]),
    }
}

#MPTT Settings

MPTT_ADMIN_LEVEL_INDENT = 30

AUTHENTICATION_BACKENDS = (
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
)

#email configuration
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_USER = 'Tratum <no-reply@tratum.co>'
EMAIL_HOST_USER = 'apptitud'
EMAIL_HOST_PASSWORD = 'jkdsjk4534.sd!"'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Auth settings
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_CONFIRMATION_ANONYMOUS_REDIRECT_URL = '/'
ACCOUNT_EMAIL_CONFIRMATION_AUTHENTICATED_REDIRECT_URL = '/'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_ADAPTER = 'users.adapters.AccountAdapter'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
SOCIALACCOUNT_QUERY_EMAIL = True
LOGOUT_ON_PASSWORD_CHANGE = True
OLD_PASSWORD_FIELD_ENABLED = True


#Social account settings
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'https'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'first_name',
            'last_name',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': lambda request: 'es_CO',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v2.12'
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    }
}

#facebook
SOCIAL_AUTH_FACEBOOK_KEY = '1124600941010990'  # App ID
SOCIAL_AUTH_FACEBOOK_SECRET ='5072f4a65001e6ac0a272cc17d8fd4eb' #app key
SOCIALACCOUNT_EMAIL_VERIFICATION = 'none'
SOCIALACCOUNT_ADAPTER = 'users.adapters.SocialAccountAdapter'

# DRF Config
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'api.permissions.HasAPIAccess',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    )
}

#Raven
RAVEN_CONFIG = {
    'dsn': 'https://01d4dd1d2f3e43e9aee6a4831d69a9c7:ddd7c80b621541528f4f41c1a7bac91d@sentry.io/1282705',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.abspath(os.pardir)),
}