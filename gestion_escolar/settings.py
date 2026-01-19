import os
from pathlib import Path

# --- CONFIGURACIÓN DE RUTAS ---
# BASE_DIR es /home/tecnica283/gestion_escolar
BASE_DIR = Path(__file__).resolve().parent

# --- SEGURIDAD ---
SECRET_KEY = "django-insecure-_bw2ak=_qdss(m72%h0lcg#i!ma4$4i+1p90j#p^%)j46(o39q"
DEBUG = True
ALLOWED_HOSTS = ['tecnica283.pythonanywhere.com', 'localhost', '127.0.0.1']

# --- APLICACIONES ---
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "alumnos",  
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# --- CAMBIO CLAVE AQUÍ ---
# Como urls.py está en la misma carpeta que settings.py, no lleva el "gestion_escolar."
ROOT_URLCONF = "urls" 

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, 'templates')],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.media",
            ],
        },
    },
]

# --- CAMBIO CLAVE AQUÍ ---
WSGI_APPLICATION = "wsgi.application"

# --- BASE DE DATOS ---
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# --- VALIDACIÓN DE CONTRASEÑAS ---
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# --- IDIOMA Y HORA ---
LANGUAGE_CODE = "es-ar"
TIME_ZONE = "America/Argentina/Buenos_Aires"
USE_I18N = True
USE_TZ = True

# --- ARCHIVOS ESTÁTICOS Y MEDIA ---
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FILE_UPLOAD_PERMISSIONS = 0o644
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- CONFIGURACIÓN DE USUARIO PERSONALIZADO ---
AUTH_USER_MODEL = 'alumnos.Usuario'

# --- REDIRECCIONES ---
LOGIN_REDIRECT_URL = 'panel_alumno'
LOGOUT_REDIRECT_URL = 'home'
LOGIN_URL = 'login'

# --- CONFIGURACIÓN DE EMAIL ---
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ema1273@gmail.com'
EMAIL_HOST_PASSWORD = 'skbkeptwswvavcxj'
DEFAULT_FROM_EMAIL = 'ema1273@gmail.com'