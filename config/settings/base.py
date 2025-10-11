# ruff: noqa: ERA001, E501
import ssl
from pathlib import Path

import environ

# UNFOLD CONFIGURATION
# ------------------------------------------------------------------------------
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve(strict=True).parent.parent.parent
# django_template/
APPS_DIR = BASE_DIR / "django_template"
env = environ.Env()

READ_DOT_ENV_FILE = True
if READ_DOT_ENV_FILE:
    # OS environment variables take precedence over variables from .env
    env.read_env(str(BASE_DIR / ".env"))

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = env.bool("DJANGO_DEBUG", False)
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "UTC"
# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en"  # changelog-0.7.0
# https://docs.djangoproject.com/en/dev/ref/settings/#languages
# from django.utils.translation import gettext_lazy as _
# changelog-0.7.0
LANGUAGES = [
    ("en", _("English")),
    ("pl", _("Polish")),
    ("de", _("German")),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# changelog-0.7.0
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True
# https://docs.djangoproject.com/en/dev/ref/settings/#locale-paths
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# DATABASES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {"default": env.db("DATABASE_URL")}
DATABASES["default"]["ATOMIC_REQUESTS"] = True
# https://docs.djangoproject.com/en/stable/ref/settings/#std:setting-DEFAULT_AUTO_FIELD
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# URLS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = "config.urls"
# https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = "config.wsgi.application"

# UNFOLD
# ------------------------------------------------------------------------------
# Modern Django admin interface built with Tailwind CSS.
UNFOLD_APPS = [
    "unfold",  # Core Unfold theme and admin UI replacement
    "unfold.contrib.filters",  # Advanced sidebar filters with form inputs
    "unfold.contrib.forms",  # Styled form widgets matching Unfold theme
    "unfold.contrib.inlines",  # Collapsible and tabbed inlines in admin
    "unfold.contrib.import_export",  # Integration with django-import-export
    "unfold.contrib.guardian",  # Integration with django-guardian (object permissions)
    "unfold.contrib.simple_history",  # Integration with django-simple-history
    "unfold.contrib.location_field",  # Integration with django-location-field
    "unfold.contrib.constance",  # Integration with django-constance (dynamic settings)
    "location_field.apps.DefaultConfig",
]
# APPS
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # "django.contrib.humanize", # Handy template tags
    "django.contrib.admin",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "crispy_forms",
    "crispy_bootstrap5",
    "allauth",
    "allauth.account",
    "allauth.mfa",
    "allauth.socialaccount",
    # "allauth.socialaccount.providers.google",
    # "allauth.socialaccount.providers.github",
    # "allauth.socialaccount.providers.openid_connect",
    "django_celery_beat",
    "rest_framework",
    "rest_framework.authtoken",
    "corsheaders",
    "drf_spectacular",
    # wagtail
    "wagtail.contrib.forms",
    "wagtail.contrib.redirects",
    "wagtail.embeds",
    "wagtail.sites",
    "wagtail.users",
    "wagtail.snippets",
    "wagtail.documents",
    "wagtail.images",
    "wagtail.search",
    "wagtail.admin",
    "wagtail",
    "modelcluster",
    "taggit",
    # Your stuff:
    "import_export",
    "schema_viewer",
    "auditlog",
    "data_browser",
    "django_cotton",  # https://django-cotton.com/docs/quickstart
]
LOCAL_APPS = [
    "django_template.users",
    # Your stuff: custom apps go here
    "django_template.apps.shared",
    "django_template.apps.api",
    "django_template.apps.web",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = UNFOLD_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "django_template.contrib.sites.migrations"}

# AUTHENTICATION
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = "users:redirect"
# https://docs.djangoproject.com/en/dev/ref/settings/#login-url
LOGIN_URL = "account_login"

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
# https://docs.djangoproject.com/en/dev/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# MIDDLEWARE
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#middleware
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
    # auditlog
    "auditlog.middleware.AuditlogMiddleware",
    # wagtail
    "wagtail.contrib.redirects.middleware.RedirectMiddleware",
]

# STATIC
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(BASE_DIR / "staticfiles")
# https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = "/static/"
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR / "static"),
    str(APPS_DIR / "apps" / "web" / "static"),
]
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# MEDIA
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = str(APPS_DIR / "media")
# https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = "/media/"

# WAGTAIL
# https://docs.wagtail.org/en/stable/getting_started/integrating_into_django.html
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10_000
WAGTAIL_SITE_NAME = "My Example Site"
WAGTAILADMIN_BASE_URL = "http://example.com"
WAGTAILDOCS_EXTENSIONS = [
    "csv",
    "docx",
    "key",
    "odt",
    "pdf",
    "pptx",
    "rtf",
    "txt",
    "xlsx",
    "zip",
]

# TEMPLATES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#templates
TEMPLATES = [
    {
        # https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-TEMPLATES-BACKEND
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        # https://docs.djangoproject.com/en/dev/ref/settings/#dirs
        "DIRS": [
            str(APPS_DIR / "templates"),
            str(APPS_DIR / "apps" / "web" / "templates"),
        ],
        # https://docs.djangoproject.com/en/dev/ref/settings/#app-dirs
        "APP_DIRS": True,
        "OPTIONS": {
            # https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                "django_template.users.context_processors.allauth_settings",
            ],
        },
    },
]

# https://docs.djangoproject.com/en/dev/ref/settings/#form-renderer
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# http://django-crispy-forms.readthedocs.io/en/latest/install.html#template-packs
# changelog-0.7.0
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5", "unfold_crispy"]
# Use Bootstrap by default.
CRISPY_TEMPLATE_PACK = "bootstrap5"

# FIXTURES
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#fixture-dirs
FIXTURE_DIRS = (str(APPS_DIR / "fixtures"),)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-httponly
SESSION_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-httponly
CSRF_COOKIE_HTTPONLY = True
# https://docs.djangoproject.com/en/dev/ref/settings/#x-frame-options
X_FRAME_OPTIONS = "DENY"

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND",
    default="django.core.mail.backends.smtp.EmailBackend",
)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-timeout
EMAIL_TIMEOUT = 5

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL.
ADMIN_URL = "admin/"
# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [("""Sean Njela""", "sean-njela@devopssean.netlify.app")]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
# https://cookiecutter-django.readthedocs.io/en/latest/settings.html#other-environment-settings
# Force the `admin` sign in process to go through the `django-allauth` workflow
DJANGO_ADMIN_FORCE_ALLAUTH = env.bool("DJANGO_ADMIN_FORCE_ALLAUTH", default=False)

# LOGGING
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#logging
# See https://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

REDIS_URL = env("REDIS_URL", default="redis://redis:6379/0")
REDIS_SSL = REDIS_URL.startswith("rediss://")

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-timezone
    CELERY_TIMEZONE = TIME_ZONE
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-broker_url
CELERY_BROKER_URL = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_backend
CELERY_RESULT_BACKEND = REDIS_URL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#redis-backend-use-ssl
CELERY_REDIS_BACKEND_USE_SSL = CELERY_BROKER_USE_SSL
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-extended
CELERY_RESULT_EXTENDED = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-always-retry
# https://github.com/celery/celery/pull/6122
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#result-backend-max-retries
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-accept_content
CELERY_ACCEPT_CONTENT = ["json"]
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-task_serializer
CELERY_TASK_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std:setting-result_serializer
CELERY_RESULT_SERIALIZER = "json"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_TIME_LIMIT = 5 * 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#task-soft-time-limit
# TODO: set to whatever value is adequate in your circumstances
CELERY_TASK_SOFT_TIME_LIMIT = 60
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#beat-scheduler
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-send-task-events
CELERY_WORKER_SEND_TASK_EVENTS = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#std-setting-task_send_sent_event
CELERY_TASK_SEND_SENT_EVENT = True
# https://docs.celeryq.dev/en/stable/userguide/configuration.html#worker-hijack-root-logger
CELERY_WORKER_HIJACK_ROOT_LOGGER = False
# django-allauth
# ------------------------------------------------------------------------------
ACCOUNT_ALLOW_REGISTRATION = env.bool("DJANGO_ACCOUNT_ALLOW_REGISTRATION", True)
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_LOGIN_METHODS = {"email"}
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_SIGNUP_FIELDS = ["email*"]
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
# https://docs.allauth.org/en/latest/account/configuration.html
ACCOUNT_ADAPTER = "django_template.users.adapters.AccountAdapter"
# https://docs.allauth.org/en/latest/account/forms.html
ACCOUNT_FORMS = {"signup": "django_template.users.forms.UserSignupForm"}
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_ADAPTER = "django_template.users.adapters.SocialAccountAdapter"
# https://docs.allauth.org/en/latest/socialaccount/configuration.html
SOCIALACCOUNT_FORMS = {"signup": "django_template.users.forms.UserSocialSignupForm"}
# # ------------------------------------------------------------------------------
# # SOCIAL ACCOUNT PROVIDERS
# # ------------------------------------------------------------------------------

# SOCIALACCOUNT_AUTO_SIGNUP = True
# SOCIALACCOUNT_EMAIL_VERIFICATION = "optional"
# SOCIALACCOUNT_STORE_TOKENS = True
# SOCIALACCOUNT_QUERY_EMAIL = True
# SOCIALACCOUNT_REQUESTS_TIMEOUT = 5

# Provider configurations
SOCIALACCOUNT_PROVIDERS = {
    # "google": {
    #     "SCOPE": ["profile", "email"],
    #     "AUTH_PARAMS": {"access_type": "online"},
    #     "OAUTH_PKCE_ENABLED": True,
    #     "FETCH_USERINFO": True,
    #     "APP": {
    #         "client_id": env("GOOGLE_CLIENT_ID", default=""),
    #         "secret": env("GOOGLE_CLIENT_SECRET", default=""),
    #         "key": "",
    #     },
    # },
    # "github": {
    #     "VERIFIED_EMAIL": True,
    #     "APP": {
    #         "client_id": env("GITHUB_CLIENT_ID", default=""),
    #         "secret": env("GITHUB_CLIENT_SECRET", default=""),
    #         "key": "",
    #     },
    # },
    # "openid_connect": {
    #     "OAUTH_PKCE_ENABLED": True,
    #     "APPS": [
    #         {
    #             "provider_id": "auth0",
    #             "name": "Auth0",
    #             "client_id": env("AUTH0_CLIENT_ID"),
    #             "secret": env("AUTH0_CLIENT_SECRET"),
    #             "settings": {
    #                 # Must be your tenant base URL
    #                 "server_url": f"https://{env('AUTH0_DOMAIN')}",
    #                 "fetch_userinfo": True,
    #                 "oauth_pkce_enabled": True,
    #                 # Use basic unless Auth0 specifically requires post
    #                 "token_auth_method": "client_secret_basic",
    #                 "scope": ["openid", "profile", "email"],
    #             },
    #         },
    #     ],
    # },
}
# Magic login
# Disable normal verification links, rely on code login flow only
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_EMAIL_VERIFICATION_BY_CODE_ENABLED = False
# ACCOUNT_LOGIN_BY_CODE_ENABLED = True  # Enables email code login
ACCOUNT_LOGIN_BY_CODE_REQUIRED = True  # Optional: keep password login also active
ACCOUNT_LOGIN_BY_CODE_MAX_ATTEMPTS = 3  # Number of allowed code entry attempts
ACCOUNT_LOGIN_BY_CODE_TIMEOUT = 180  # Code validity in seconds
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
ACCOUNT_PREVENT_ENUMERATION = True

# django-rest-framework
# -------------------------------------------------------------------------------
# django-rest-framework - https://www.django-rest-framework.org/api-guide/settings/
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.TokenAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAuthenticated",),
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# django-cors-headers - https://github.com/adamchainz/django-cors-headers#setup
CORS_URLS_REGEX = r"^/api/.*$"

# By Default swagger ui is available only to admin user(s). You can change permission classes to change that
# See more configuration options at https://drf-spectacular.readthedocs.io/en/latest/settings.html#settings
SPECTACULAR_SETTINGS = {
    "TITLE": "Django Template API",
    "DESCRIPTION": "Documentation of API endpoints of Django Template",
    "VERSION": "1.0.0",
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAdminUser"],
    "SCHEMA_PATH_PREFIX": "/api/",
}
# Your stuff...
# ------------------------------------------------------------------------------

# UNFOLD CONFIGURATION
# ------------------------------------------------------------------------------
#
# Configuration dictionary controlling all Unfold admin interface options.

# This section defines Unfolds behaviour, UI appearance, and feature extensions.
# Each setting affects different aspects of the admin — from theming and layout
# to integrations, language switching, and sidebar navigation.

# The configuration is declarative, allowing Unfold to dynamically adapt the
# admin without manual HTML or template overrides.
#

UNFOLD = {
    # ------------------------------------------------------------------
    # Site Identity and Branding
    # ------------------------------------------------------------------
    "SITE_TITLE": "Django Template Admin",  # Page title (HTML <title> tag)
    "SITE_HEADER": "Django Template",  # Main heading in admin UI
    "SITE_SUBHEADER": "Administration Panel",  # Secondary title displayed under the header
    # Dropdown links available in the admins header bar
    "SITE_DROPDOWN": [
        {
            "icon": "diamond",  # Icon displayed in the dropdown
            "title": _("Website"),  # Label shown to users
            "link": "https://devopssean.netlify.app",  # External link
        },
        {
            "icon": "code",
            "title": _("Source"),
            "link": "https://github.com/sean-njela/django_template/",
        },
    ],
    "SITE_URL": "/",  # Root admin URL
    "SHOW_LANGUAGES": True,  # Displays language selector in the header
    # ------------------------------------------------------------------
    # Language Configuration
    # ------------------------------------------------------------------
    "LANGUAGES": {
        # Controls which languages appear in the navigation dropdown
        "navigation": [
            {
                "bidi": False,  # Indicates whether text direction is bidirectional
                "code": "en",
                "name": "English",
                "name_local": "English",  # Localised self-name
                "name_translated": _("English"),
            },
            {
                "bidi": False,
                "code": "pl",
                "name": "Polish",
                "name_local": "Polski",
                "name_translated": _("Polish"),
            },
            {
                "bidi": False,
                "code": "de",
                "name": "German",
                "name_local": "Deutsch",
                "name_translated": _("German"),
            },
        ],
    },
    # ------------------------------------------------------------------
    # Visual Branding (optional icons and logos)
    # ------------------------------------------------------------------
    # Example usage:
    # "SITE_ICON": {
    #     "light": lambda request: static("icons/icon-light.svg"),
    #     "dark": lambda request: static("icons/icon-dark.svg"),
    # },
    # "SITE_LOGO": {
    #     "light": lambda request: static("icons/logo-light.svg"),
    #     "dark": lambda request: static("icons/logo-dark.svg"),
    # },
    # "SITE_SYMBOL": "speed",
    # "SITE_FAVICONS": [
    #     {
    #         "rel": "icon",
    #         "sizes": "32x32",
    #         "type": "image/svg+xml",
    #         "href": lambda request: static("icons/favicon.svg"),
    #     },
    # ],
    # ------------------------------------------------------------------
    # Core Admin Behaviour Toggles
    # ------------------------------------------------------------------
    "SHOW_HISTORY": True,  # Enables object change history tracking
    "SHOW_VIEW_ON_SITE": True,  # Adds "View on site" link for objects
    "SHOW_BACK_BUTTON": True,  # Adds a back button in form views
    # Dynamic callbacks loaded from django_template/admin_config.py
    # These are Python import paths to callable functions.
    "ENVIRONMENT": "django_template.admin_config.environment_callback",
    "ENVIRONMENT_TITLE_PREFIX": "django_template.admin_config.environment_title_prefix_callback",
    "DASHBOARD_CALLBACK": "django_template.admin_config.dashboard_callback",
    # ------------------------------------------------------------------
    # Theme and UI Customisation
    # ------------------------------------------------------------------
    "THEME": None,  # Allows user toggle between light/dark themes
    "THEME_DEFAULT": "dark",  # Default visual mode if user preference not set
    "BORDER_RADIUS": "4px",  # Base corner rounding applied to all UI components
    # Optional theme-level overrides for custom CSS or JS
    # "LOGIN": {
    #     "image": lambda request: static("img/login-bg.jpg"),
    #     "redirect_after": lambda request: reverse_lazy("admin:index"),
    # },
    # "STYLES": [
    #     lambda request: static("css/custom-admin.css"),
    # ],
    # "SCRIPTS": [
    #     lambda request: static("js/custom-admin.js"),
    # ],
    # ------------------------------------------------------------------
    # Custom Colour Palette
    # ------------------------------------------------------------------
    # Defines Tailwind-compatible RGB colour variables used by Unfold.
    # Each key represents a semantic colour group (base, primary, warning, etc.).
    "COLORS": {
        # ------------------------------------------------------------------
        # Base Neutral Palette
        # ------------------------------------------------------------------
        # Neutral greys used for backgrounds, borders, and layout structure.
        # 50-300: light background shades.
        # 700-950: dark neutral tones for contrast and dark mode.
        "base": {
            "50": "235 235 235",  # Very light grey, primary background (light mode)
            "100": "230 230 230",  # Slightly darker base background
            "200": "220 220 220",  # Border or divider tone
            "300": "210 210 210",  # Muted section divider
            "700": "65 65 65",  # Mid-dark neutral for dark mode elements
            "800": "55 55 55",  # Darker surface tone in dark mode
            "900": "45 45 45",  # Main dark background tone
            "950": "35 35 35",  # Deep black-grey for dark mode base
        },
        # ------------------------------------------------------------------
        # Primary Palette
        # ------------------------------------------------------------------
        # Used for brand accents, primary buttons, and key interactive elements.
        # Represents cool blue tones.
        "primary": {
            "50": "235 240 255",  # Ultra light blue tint (hover backgrounds)
            "100": "220 230 255",  # Light hover or subtle highlight
            "200": "200 215 255",  # Input focus border
            "300": "175 195 255",  # Secondary button hover
            "400": "140 160 255",  # Button background
            "500": "110 135 255",  # Primary brand colour
            "600": "90 120 230",  # Slightly darker for active states
            "700": "75 100 200",  # Focus ring or strong borders
            "800": "60 80 160",  # Deep accent for dark mode
            "900": "45 65 130",  # Text or border accent (dark mode)
        },
        # ------------------------------------------------------------------
        # Secondary Palette
        # ------------------------------------------------------------------
        # Soft purple-grey tones for secondary UI highlights or muted branding.
        "secondary": {
            "50": "240 230 240",  # Light lavender background
            "100": "225 210 225",  # Subtle secondary hover
            "200": "200 185 200",  # Input borders or secondary focus
            "300": "175 155 175",  # Muted divider or background
            "400": "150 130 150",  # Secondary hover active state
            "500": "130 110 130",  # Main secondary tone
            "600": "105 90 105",  # Muted dark purple for text
            "700": "85 70 85",  # Darker version for dark mode
            "800": "60 45 60",  # Deep background
            "900": "40 30 40",  # Very dark neutral purple
        },
        # ------------------------------------------------------------------
        # Accent Palette
        # ------------------------------------------------------------------
        # Soft desaturated blue-grey tones used for subtle decorative accents.
        "accent": {
            "50": "230 240 245",  # Very light bluish-grey background
            "100": "215 230 240",  # Highlight box background
            "200": "190 210 225",  # Accent background shading
            "300": "160 180 200",  # Muted blue-grey borders
            "400": "135 155 175",  # Hover highlight
            "500": "115 135 155",  # Main accent tone
            "600": "95 115 130",  # Slightly darker hover colour
            "700": "75 90 105",  # Text for disabled elements
            "800": "60 70 85",  # Deep accent for dark mode
            "900": "45 50 65",  # Dark background contrast
        },
        # ------------------------------------------------------------------
        # Success Palette
        # ------------------------------------------------------------------
        # Shades of green for positive feedback, confirmation messages, and success states.
        "success": {
            "50": "200 240 200",  # Light green background for success alerts
            "100": "170 220 170",  # Subtle green tint
            "200": "140 200 140",  # Confirm state highlight
            "300": "110 180 110",  # Hover background for success button
            "400": "85 160 85",  # Mid-tone green
            "500": "65 135 65",  # Default success colour
            "600": "50 110 50",  # Active/pressed state
            "700": "40 90 40",  # Text in dark mode success state
            "800": "30 70 30",  # Deep success background
            "900": "20 50 20",  # Very dark green for emphasis
        },
        # ------------------------------------------------------------------
        # Info Palette
        # ------------------------------------------------------------------
        # Blue tones for informational messages and neutral notifications.
        "info": {
            "50": "200 220 240",  # Light blue background for info alerts
            "100": "170 200 230",  # Hover state
            "200": "140 180 220",  # Light info border
            "300": "110 150 200",  # Mid-tone background
            "400": "90 125 180",  # Info button hover
            "500": "70 100 160",  # Main info colour
            "600": "55 80 140",  # Active state
            "700": "40 60 110",  # Text or accent border
            "800": "30 45 85",  # Dark background info tone
            "900": "20 30 60",  # Deep info contrast
        },
        # ------------------------------------------------------------------
        # Warning Palette
        # ------------------------------------------------------------------
        # Yellow-orange tones used for cautionary messages or alerts.
        "warning": {
            "50": "255 245 200",  # Very light yellow warning background
            "100": "255 230 170",  # Hover highlight
            "200": "255 210 140",  # Border highlight
            "300": "255 190 110",  # Warning hover background
            "400": "240 160 80",  # Mid-tone amber
            "500": "220 130 60",  # Default warning colour
            "600": "190 100 45",  # Active pressed state
            "700": "160 80 30",  # Strong amber for dark mode
            "800": "120 60 20",  # Deep tone for contrast
            "900": "90 40 15",  # Dark warning background
        },
        # ------------------------------------------------------------------
        # Error Palette
        # ------------------------------------------------------------------
        # Red tones for error messages, form validation, and destructive actions.
        "error": {
            "50": "240 200 200",  # Light red alert background
            "100": "230 170 170",  # Subtle red tint
            "200": "215 140 140",  # Border or notification colour
            "300": "190 110 110",  # Button hover or form error
            "400": "160 85 85",  # Main red tone
            "500": "135 65 65",  # Primary error colour
            "600": "110 50 50",  # Active/pressed error state
            "700": "90 40 40",  # Dark text on light backgrounds
            "800": "65 30 30",  # Dark background error accent
            "900": "45 20 20",  # Deep error background
        },
        # ------------------------------------------------------------------
        # Font Palette
        # ------------------------------------------------------------------
        # Defines font colour contrast in both light and dark themes.
        "font": {
            "subtle-light": "120 120 120",  # Secondary text on light background
            "default-light": "0 0 0",  # Standard dark text for light theme
            "important-light": "0 0 0",  # Emphasised text in light mode
            "subtle-dark": "170 170 170",  # Secondary text for dark backgrounds
            "default-dark": "240 240 240",  # Default light text in dark mode
            "important-dark": "255 255 255",  # Brightest text colour for contrast
        },
    },
    # ------------------------------------------------------------------
    # Plugin Extensions
    # ------------------------------------------------------------------
    # Enables Unfolds integrations with third-party libraries.
    "EXTENSIONS": {
        "modeltranslation": {
            # Maps language codes to emoji flags used in translation tabs
            "flags": {
                "en": "🇬🇧",
                "pl": "🇵🇱",
                "de": "🇩🇪",
            },
        },
    },
    # ------------------------------------------------------------------
    # Sidebar Navigation
    # ------------------------------------------------------------------
    # Controls visibility, search, and hierarchical structure of the admin sidebar.
    "SIDEBAR": {
        "show_search": True,  # Enables the sidebar search bar
        "command_search": False,  # Disables command palette shortcut
        "show_all_applications": True,  # Displays all Django apps by default
        # Custom navigation items organised under labelled sections
        "navigation": [
            {
                "title": _("Navigation"),
                "separator": True,  # Adds a visual separator line
                "collapsible": False,  # Allows section collapse/expand
                "items": [
                    {
                        "title": _("Dashboard"),
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                        "badge": "django_template.admin_config.badge_callback",
                        "permission": lambda request: request.user.is_superuser,
                    },
                    {
                        "title": _("Users"),
                        "icon": "people",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": _("Groups"),
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
    # ------------------------------------------------------------------
    # Tabbed Navigation
    # ------------------------------------------------------------------
    # Defines context-aware tabs for specific model admin views.
    "TABS": [
        {
            "models": ["users.user"],  # Applies to the User model admin
            "items": [
                {
                    "title": _("User Management"),
                    "link": reverse_lazy("admin:users_user_changelist"),
                    "permission": "django_template.admin_config.permission_callback",
                },
            ],
        },
    ],
}
