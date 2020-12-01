# Based on Developer Setup, with Area Access and Kiosk apps enabled, login button shown, and UWaterloo SMTP server set up
# Does NOT include WatIAM authentication set up by FAST group

# -------------------- Django settings for NEMO --------------------
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# To enable interlocks
INTERLOCKS_ENABLED = True

# Core settings
DEBUG = True
AUTH_USER_MODEL = 'NEMO.User'
WSGI_APPLICATION = 'NEMO.wsgi.application'
ROOT_URLCONF = 'NEMO.urls'

# Authentication
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'login'

# Date and time formats
DATETIME_FORMAT = "l, F jS, Y @ g:i A"
DATE_FORMAT = "m/d/Y"
TIME_FORMAT = "g:i A"
DATETIME_INPUT_FORMATS = ['%m/%d/%Y %I:%M %p']
DATE_INPUT_FORMATS = ['%m/%d/%Y']
TIME_INPUT_FORMATS = ['%I:%M %p']

USE_I18N = False
USE_L10N = False
USE_TZ = True

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'NEMO',
    'rest_framework',
    'rest_framework.authtoken',
    'django_filters',
    'mptt',
    # To enable Area Access and Kiosk apps
    'NEMO.apps.area_access',
    'NEMO.apps.kiosk',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'NEMO.middleware.SessionTimeout',
    # Add a middleware to identify when the user's session has expired. This works in conjunction with LDAPS authentication on the public facing web server. Kerberos does not need this middleware on the internal facing web server.
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'NEMO.middleware.HTTPHeaderAuthenticationMiddleware',
    # RemoteUser middleware to authenticate using env var REMOTE_USER
    'NEMO.middleware.RemoteUserAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.common.BrokenLinkEmailsMiddleware',
    'NEMO.middleware.DeviceDetectionMiddleware',
    'NEMO.middleware.ImpersonateMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                #'NEMO.context_processors.hide_logout_button',
                'NEMO.context_processors.show_logout_button',
                # Add a 'request context processor' in order to figure out whether to display the logout button. If the site is configured to use the LDAP authentication backend (public facing NEMO) then we want to provide a logoff button (in the menu bar). Otherwise the Kerberos authentication backend is used (internal to NIST) and no logoff button is necessary.
                'NEMO.context_processors.base_context',
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# -------------------- Third party Django addons for NEMO --------------------
# These are third party capabilities that NEMO employs. They are documented on
# the respective project sites. Only customize these if you know what you're doing.

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('NEMO.permissions.BillingAPI',),
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'DEFAULT_AUTHENTICATION_CLASSES': ('rest_framework.authentication.TokenAuthentication',),
}

# ------------ Organization specific settings (officially supported by Django) ------------
# Customize these to suit your needs. Documentation can be found at:
# https://docs.djangoproject.com/en/1.11/ref/settings/

ALLOWED_HOSTS = ['localhost', '0.0.0.0']

SERVER_EMAIL = 'NEMO Server Administrator <nemo.admin@nist.gov>'

ADMINS = []
MANAGERS = ADMINS

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_FILE_PATH = os.path.join(BASE_DIR, 'email_sink/')

#  UW Email SMTP
EMAIL_HOST = 'mailservices.uwaterloo.ca'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True

TIME_ZONE = 'America/New_York'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'nemo.db'),
    }
}

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'resources/icons')
MEDIA_URL = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'test'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': 'NEMO %(levelname)s %(message)s',
        },
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            'datefmt': "%d/%b/%Y %H:%M:%S",
        },
        'simple': {
            'format': '[%(asctime)s] %(name)s %(levelname)s %(message)s',
            'datefmt': '%d/%b/%Y %H:%M:%S'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'nemo.log'),
            'formatter': 'simple',
        },
        'console': {
            'formatter': 'simple',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        '': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'WARNING',
            'propagate': True,
        },
        'NEMO': {
            'level': 'DEBUG',
            'handlers': ['file', 'console'],
            'propagate': True,
        },
        'django': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# ------------ Organization specific settings (NEMO specific; NOT supported by Django) ------------
# Customize these to suit your needs

# When true, all available URLs and NEMO functionality is enabled.
# When false, conditional URLs are removed to reduce the attack surface of NEMO.
# Reduced functionality for NEMO is desirable for the public facing version
# of the site in order to mitigate security risks.
ALLOW_CONDITIONAL_URLS = True

# When true, interlock function will be enabled and request will be made to lock/unlock interlocks.
# When false, the feature will be disabled
INTERLOCKS_ENABLED = True

# There are two options to authenticate users:
#   1) A decoupled "REMOTE_USER" method (such as Kerberos authentication from a reverse proxy)
#   2) LDAP authentication from NEMO itself
# AUTHENTICATION_BACKENDS = ['NEMO.views.authentication.LDAPAuthenticationBackend']
AUTHENTICATION_BACKENDS = ['NEMO.views.authentication.RemoteUserAuthenticationBackend']
# AUTHENTICATION_BACKENDS = ['NEMO.views.authentication.NginxKerberosAuthorizationHeaderAuthenticationBackend']