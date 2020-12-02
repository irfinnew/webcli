"""
Django settings for the WebCLI project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

import os
import socket
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def parse_bool(value):
	return {'true': True, 'false': False}[str(value).lower()]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

DEBUG = parse_bool(os.environ['CY_DEBUG'])
ENV_NAME = os.environ.get('CY_ENV_NAME', socket.getfqdn())

# SECURITY WARNING: keep the secret key used in production secret!
if DEBUG:
	SECRET_KEY = 'W7iFfH'
else:
	SECRET_KEY = os.environ['CY_SECRET_KEY']
	if len(SECRET_KEY) < 32:
		raise Exception('Secret key should be at least 32 characters')

# Access control happens in the webserver, not here.
ALLOWED_HOSTS = ['*']

SESSION_COOKIE_SECURE = parse_bool(os.environ.get('CY_SECURE_COOKIES', False))
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE

# Application definition

INSTALLED_APPS = (
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'cli',
)

MIDDLEWARE_CLASSES = (
	'request_id.middleware.RequestIdMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
	# Stuff we either do ourselves in the front-end webserver or don't want at all.
	#'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'webcli.urls'

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

WSGI_APPLICATION = 'webcli.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': os.environ['CY_DB_DRIVER'],
		'NAME': os.environ['CY_DB_NAME'],
		'USER': os.environ.get('CY_DB_USER', ''),
		'HOST': os.environ.get('CY_DB_HOST', ''),
		'PORT': os.environ.get('CY_DB_PORT', ''),
		'PASSWORD': os.environ.get('CY_DB_PASSWORD', ''),
		'CONN_MAX_AGE': 300,
	},
}

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# Use system time zone
TIME_ZONE = None

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, '../static'),
)

# Bit of a hack, but seems to work well enough.
# The default format is stupid anyway.
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y-m-d H:i:s (D)"

MEDIA_ROOT = os.path.abspath(os.environ['CY_MEDIA_ROOT'])

REQUEST_ID_HEADER = None

if not DEBUG:
	SERVER_EMAIL = os.environ['CY_ERROR_EMAIL_FROM']
	ADMINS = ((addr, addr) for addr in os.environ['CY_ERROR_EMAIL_TO'].split())

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'request_id': {
			'()': 'request_id.logging.RequestIdFilter',
		},
		'require_debug_false': {
			'()': 'django.utils.log.RequireDebugFalse',
		},
		'require_debug_true': {
			'()': 'django.utils.log.RequireDebugTrue',
		},
	},
	'formatters': {
		'verbose': {
			'format': '%(asctime)s [%(request_id)s] %(module)s %(levelname)s: %(message)s',
		},
	},
	'handlers': {
		'mail_admins': {
			'level': 'ERROR',
			'class': 'django.utils.log.AdminEmailHandler',
			'formatter': 'verbose',
			'filters': ['request_id', 'require_debug_false'],
		},
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'verbose',
			'filters': ['request_id', 'require_debug_true'],
		},
		'file': {
			'level': os.environ['CY_LOGFILE_LEVEL'],
			'class': 'logging.handlers.WatchedFileHandler',
			'filename': os.path.abspath(os.environ['CY_LOGFILE_PATH']),
			'formatter': 'verbose',
			'filters': ['request_id'],
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console', 'file', 'mail_admins'],
			'level': 'WARNING',
			'propagate': True,
		},
		'cli': {
			'handlers': ['console', 'file', 'mail_admins'],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}
