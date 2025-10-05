# **Changelog 0.7.0 – Django Template**

**Date:** 2025-10-05

## **Release highlights**

* Added **Unfold admin interface** with Tailwind-based theming.
* Implemented **multi-language (i18n)** system for English, Polish, and German.
* Integrated **Crispy Forms (unfold_crispy)** for styled admin and Allauth forms.
* Re-architected `admin.py` inheritance to use `unfold.admin.ModelAdmin`.
* Added theme toggle with **dark (default)** and **light (#FAF7F5)** modes.
* Unified custom admin CSS/JS and login theming.
* Added **callback functions** for dashboard, environment, and sidebar badges.

## **Added**

### **1. Unfold installation and integration**

Install:

```bash
uv add django-unfold
```

Then add to `INSTALLED_APPS` (must come before Django admin):

```python
UNFOLD_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    "unfold.contrib.import_export",
    "unfold.contrib.guardian",
    "unfold.contrib.simple_history",
    "unfold.contrib.location_field",
    "unfold.contrib.constance",
]
INSTALLED_APPS = UNFOLD_APPS + DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```

These provide:

* Filters and styled widgets
* Collapsible inlines
* Optional integrations (guardian, simple_history, constance)

### **2. New admin configuration (admin.py)**

```python
from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin

from .forms import UserAdminChangeForm, UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)

@admin.register(User)
class UserAdmin(auth_admin.UserAdmin, ModelAdmin):
    """Combines Django’s logic with Unfold’s styling."""
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    ordering = ["id"]

# Re-register Group with Unfold
admin.site.unregister(Group)
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Ensures Unfold styling for built-in Group model."""
    pass
```

### **3. Unfold configuration in `base.py`**

Added a full `UNFOLD = {}` configuration block:

```python
UNFOLD = {
    "SITE_TITLE": "Django Template Admin",
    "SITE_HEADER": "Django Template",
    "SITE_SUBHEADER": "Administration Panel",
    "SHOW_LANGUAGES": True,
    "LANGUAGES": {
        "navigation": [
            {"code": "en", "name": "English", "name_local": "English"},
            {"code": "pl", "name": "Polish", "name_local": "Polski"},
            {"code": "de", "name": "German", "name_local": "Deutsch"},
        ],
    },
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": True,
    "ENVIRONMENT": "django_template.admin_config.environment_callback",
    "DASHBOARD_CALLBACK": "django_template.admin_config.dashboard_callback",
    "THEME": None,               # Enables toggle
    "THEME_DEFAULT": "dark",     # Default view
    "BORDER_RADIUS": "10px",
    "COLORS": {
        "base": {
            "50": "#FAF7F5",
            "100": "#F3F0EE",
            "200": "#E6E2DF",
            "300": "#D0CCC8",
            "700": "#222222",
            "800": "#1C1C1C",
            "900": "#171717",
            "950": "#101010",
        },
        "primary": {
            "50": "#E0F4FF",
            "100": "#B8E3FF",
            "200": "#8AD1FF",
            "300": "#5BBEFF",
            "400": "#37B0F8",
            "500": "#2AA5F4",
            "600": "#198CD7",
            "700": "#1479BE",
            "800": "#0F66A5",
            "900": "#0B548C",
        },
        "font": {
            "subtle-light": "#666666",
            "default-light": "#222222",
            "important-light": "#000000",
            "subtle-dark": "#9D9D9D",
            "default-dark": "#EDEDED",
            "important-dark": "#FFFFFF",
        },
    },
}
```

This enables dark/light modes, proper contrast in dropdowns, and custom blue accent (#2AA5F4).

### **4. Admin callbacks (`admin_config.py`)**

```python
def dashboard_callback(request, context):
    context.update({"project": "Django Template"})
    return context

def environment_callback(request):
    return ["Production", "success"]

def environment_title_prefix_callback(request):
    return "[Production] "

def badge_callback(request):
    return 3 if request.user.is_superuser else None

def permission_callback(request):
    return request.user.is_authenticated and request.user.is_staff
```

These drive Unfold’s dynamic admin banner, badge counts, and sidebar logic.

### **5. Internationalisation**

**Settings additions in `base.py`:**

```python
LANGUAGE_CODE = "en"
USE_I18N = True
USE_L10N = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]
LANGUAGES = [
    ("en", _("English")),
    ("pl", _("Polish")),
    ("de", _("German")),
]
```

**URL configuration in `urls.py`:**

```python
from django.conf.urls.i18n import i18n_patterns
from django.urls import include, path
from django.conf import settings
from django.views.generic import TemplateView

urlpatterns = [
    path("i18n/", include("django.conf.urls.i18n")),
]

urlpatterns += i18n_patterns(
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("users/", include("django_template.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
)
```

### **6. Forms integration**

Updated `forms.py` to ensure compatibility with Unfold and Allauth.

```python
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from django.contrib.auth import forms as admin_forms
from django.forms import EmailField
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User
        field_classes = {"email": EmailField}

class UserAdminCreationForm(admin_forms.AdminUserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User
        fields = ("email",)
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }

class UserSignupForm(SignupForm): pass
class UserSocialSignupForm(SocialSignupForm): pass
```

Then in settings:

```python
CRISPY_ALLOWED_TEMPLATE_PACKS = ["bootstrap5", "unfold_crispy"]
CRISPY_TEMPLATE_PACK = "unfold_crispy"
```

### **7. Custom admin styles and scripts**

```python
"STYLES": [lambda request: static("css/custom-admin.css")],
"SCRIPTS": [lambda request: static("js/custom-admin.js")],
```

Store these files in `/django_template/static/css/` and `/django_template/static/js/` for light theme tweaks (dropdowns, hover, and accent fixes).

### **8. Multilingual message generation**

To extract `.po` files:

```bash
docker compose -f docker-compose.local.yml -p local run --rm django \
  uv run django-admin makemessages -l en -l pl -l de \
  --ignore-file .makemessagesignore
```

`.makemessagesignore`:

```
venv
.venv
static
node_modules
docs
docs/_build
```

## **Changed**

* Replaced all Django `ModelAdmin` with Unfold equivalents.
* Moved Unfold configuration to main settings scope (after `INSTALLED_APPS`).
* Replaced static hard-coded language config with dynamic `SHOW_LANGUAGES`.
* Added Unfold callbacks for environment and dashboard.
* Set secure Allauth admin login.

## **Fixed**

* Fixed missing styles for Allauth form fields under Unfold.
* Fixed dropdown text contrast under dark theme.
* Fixed admin theme persistence after login.
* Fixed Celery Beat admin dropdown field styling.
* Fixed locale extraction file ownership in Docker.

## **Breaking changes**

* Any custom admin templates overriding default Django `admin/` must be rewritten for Unfold.
* All custom admin classes must subclass `unfold.admin.ModelAdmin`.
* URLs now require language prefixes (`/en/`, `/pl/`, `/de/`).
* Removed reliance on Bootstrap forms for admin—now replaced by Crispy + Unfold.

## **Security**

* Enforced HTTP-only cookies:

  ```python
  SESSION_COOKIE_HTTPONLY = True
  CSRF_COOKIE_HTTPONLY = True
  ```
* Improved Redis SSL detection.
* All admin logins now go through `allauth.account.decorators.secure_admin_login`.

## **Reference commit range**

**From:** `v0.6.9`
**To:** `v0.7.0`
**Author:** [@sean-njela](https://github.com/sean-njela)