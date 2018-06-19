import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'zbua(=8tqz9(l_wkqapp!j4@c2&qnkgtk+=4-30f+td(_gr_2w'

DEBUG = True

ALLOWED_HOSTS = [
    'localhost',
    'localhost.org',
    '138.197.86.31',
    '127.0.0.1',
    '192.168.0.16',
    '192.168.0.14'
]

INTERNAL_IPS = [
    'localhost',
    'localhost.org',
    '127.0.0.1',
    '192.168.0.16'
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',   
    'django.contrib.humanize',
    'rest_framework', 
    'debug_toolbar',
    'ckeditor',
    'mptt',
    'utils',
    'document_manager',
    'business_info',
    'store',
    'webclient'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
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
            ],
        },
    },
]

WSGI_APPLICATION = 'tratum.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
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
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "tratum/static"),
]
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'tratum/media')

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
                'name': 'forms',
                'items': ['Button']
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
            'documentsection'
        ]),
    }
}


#MPTT Settings

MPTT_ADMIN_LEVEL_INDENT = 30