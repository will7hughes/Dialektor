# Copyright 2015 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pf-@jxtojga)z+4s*uwbgjrq$aep62-thd0q7f&o77xtpka!_m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: If you deploy a Django app to production, make sure to set
# an appropriate host here.
# See https://docs.djangoproject.com/en/1.10/ref/settings/
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
	'personal',
	'django_extensions',
)

MIDDLEWARE = (
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'), os.path.join(BASE_DIR, 'templates/profile'), os.path.join(BASE_DIR, 'templates/registration')],
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

WSGI_APPLICATION = 'mysite.wsgi.application'

AUTH_USER_MODEL = "personal.CustomUser" 

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# [START dbconfig]

if os.getenv('GAE_APPLICATION', None):
	# Running production, connect to GCP instance of PostgreSQL running in CloudSQL
	# This is a centralized production environment 
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql',
			'NAME': 'polls',
			'USER': os.getenv('DATABASE_USER'),
			'PASSWORD': os.getenv('DATABASE_PASSWORD'),
			'HOST': '127.0.0.1',
			'PORT': '5432',
		}
	}
else:
	# Running development, connect to local PostgreSQL in our db Docker container
	# You must setup the database 'dialektorlocaldb' and user 'dialektoruser' in your db Docker container
	# Note that our Django app runs in the web Docker container, which is why our host is 'db' and not 'localhost'
	# This is just a local database, so the password need not be complex :)
	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.postgresql_psycopg2',
			'HOST': 'db',
			'PORT': '5432',
			'NAME': 'dialektorlocaldb',
			'USER': 'dialektoruser',
			'PASSWORD': 'password'
		}
	}
# [END dbconfig]


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/


# [START staticurl]
# Development Static url


# [END staticurl]
if os.getenv('GAE_APPLICATION', None):
	# Production Static Url
	STATIC_ROOT = 'static/'
	STATIC_URL = 'https://storage.googleapis.com/dialektor-bucket/static/'
else:
	# Development Static url
	STATICFILES_DIRS = [
		os.path.join(BASE_DIR, "static"),
		os.path.join(BASE_DIR, "media"),
	]
	STATIC_URL = '/static/'