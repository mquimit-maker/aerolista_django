# ==============================================================
#  settings.py · configuración del proyecto Django
#  Este proyecto NO usa base de datos: guarda todo en archivos JSON.
# ==============================================================
from pathlib import Path

from django.contrib.messages import constants as mensajes

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "clave-solo-para-practicas-de-clase"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    "django.contrib.messages",     # mensajes flotantes (reserva creada, errores...)
    "django.contrib.staticfiles",  # sirve el CSS de static/
    "reservas",                    # NUESTRA app
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",        # protege los formularios POST
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,   # busca reservas/templates/
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",   # no se usa, Django solo lo pide
    }
}

# Los mensajes se guardan en cookies (así no necesitamos base de datos ni sesiones)
MESSAGE_STORAGE = "django.contrib.messages.storage.cookie.CookieStorage"
MESSAGE_TAGS = {mensajes.ERROR: "danger"}   # Bootstrap llama "danger" al rojo

LANGUAGE_CODE = "es"
TIME_ZONE = "America/Guayaquil"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
