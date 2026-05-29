"""Development settings."""

from .base import *  # noqa: F401,F403

DEBUG = True

# Database — SQLite for development
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# Email backend — print to console
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Celery — run tasks synchronously in development
CELERY_TASK_ALWAYS_EAGER = True
CELERY_TASK_EAGER_PROPAGATES = True

# Allow all hosts in dev
ALLOWED_HOSTS = ["*"]
