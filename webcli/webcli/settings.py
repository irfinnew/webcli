import os
import socket
from pathlib import Path
from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

def parse_bool(value):
	return {'true': True, 'false': False}[str(value).lower()]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = Path(__file__).resolve().parent.parent



#### Core
DEBUG = parse_bool(os.environ['WEB_DEBUG'])
ENV_NAME = os.environ.get('WEB_ENV_NAME', socket.getfqdn())
if DEBUG:
	SECRET_KEY = 'for_development_only'
else:
	SECRET_KEY = os.environ['WEB_SECRET_KEY']

ALLOWED_HOSTS = ['*']  # Host checking happens in the webserver, not here.
SESSION_COOKIE_SECURE = parse_bool(os.environ.get('WEB_SECURE_COOKIES', True))
CSRF_COOKIE_SECURE = SESSION_COOKIE_SECURE



#### Application definition
INSTALLED_APPS = [
	'django.contrib.admin',
	'django.contrib.auth',
	'django.contrib.contenttypes',
	'django.contrib.sessions',
	'django.contrib.messages',
	'django.contrib.staticfiles',
	'cli.apps.CliConfig',
]

MIDDLEWARE = [
	'log_request_id.middleware.RequestIDMiddleware',
	# We do this in the front-end webserver.
	#'django.middleware.security.SecurityMiddleware',
	'django.contrib.sessions.middleware.SessionMiddleware',
	'django.middleware.common.CommonMiddleware',
	'django.middleware.csrf.CsrfViewMiddleware',
	'django.contrib.auth.middleware.AuthenticationMiddleware',
	'django.contrib.messages.middleware.MessageMiddleware',
	'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'webcli.urls'

ADMIN_PATH = os.environ.get('WEB_ADMIN_PATH', '')
if ADMIN_PATH and not ADMIN_PATH.endswith('/'):
	ADMIN_PATH += '/'

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



#### Database
DATABASES = {
	'default': {
		'ENGINE': os.environ['WEB_DB_DRIVER'],
		'NAME': os.environ['WEB_DB_NAME'],
		'USER': os.environ.get('WEB_DB_USER', ''),
		'HOST': os.environ.get('WEB_DB_HOST', ''),
		'PORT': os.environ.get('WEB_DB_PORT', ''),
		'PASSWORD': os.environ.get('WEB_DB_PASSWORD', ''),
		'CONN_MAX_AGE': 300,
	},
}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



#### Password validation
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



#### Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Hmm, I dunno
# # Use system time zone
# USE_TZ = True
# with open('/etc/timezone') as fd:
# 	TIME_ZONE = fd.read().strip()

# Bit of a hack, but seems to work well enough.
# The default format is stupid anyway.
from django.conf.locale.en import formats as en_formats
en_formats.DATETIME_FORMAT = "Y-m-d H:i:s (D)"
en_formats.DATETIME_FORMAT = "Y-m-d H:i"



#### Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = (
	os.path.join(BASE_DIR, '../static'),
)

if 'WEB_MEDIA_ROOT' in os.environ:
	MEDIA_ROOT = os.path.abspath(os.environ['WEB_MEDIA_ROOT'])



#### Logging
if not DEBUG and 'WEB_ERROR_EMAIL_FROM' in os.environ and 'WEB_ERROR_EMAIL_TO' in os.environ:
	SERVER_EMAIL = os.environ['WEB_ERROR_EMAIL_FROM']
	ADMINS = ((addr, addr) for addr in os.environ['WEB_ERROR_EMAIL_TO'].split())

LOGGING = {
	'version': 1,
	'disable_existing_loggers': False,
	'filters': {
		'request_id': {
			'()': 'log_request_id.filters.RequestIDFilter',
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
			'level': os.environ['WEB_LOGFILE_LEVEL'],
			'class': 'logging.handlers.WatchedFileHandler',
			'filename': os.path.abspath(os.environ['WEB_LOGFILE_PATH']),
			'formatter': 'verbose',
			'filters': ['request_id'],
		},
	},
	'loggers': {
		'django': {
			'handlers': ['console', 'file', 'mail_admins'],
			'level': 'INFO',
			'propagate': True,
		},
		'cli': {
			'handlers': ['console', 'file', 'mail_admins'],
			'level': 'DEBUG',
			'propagate': True,
		},
	}
}
