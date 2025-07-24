from .base import *

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Django Debug Toolbar
try:
    import debug_toolbar

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
    INTERNAL_IPS = [
        "127.0.0.1"
    ]
except ModuleNotFoundError:
    pass
