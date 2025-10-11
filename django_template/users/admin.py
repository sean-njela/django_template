"""Unfold-enhanced Django admin integrating authentication, Celery scheduling,
and social account models.

This module replaces Djangos default admin styling and behaviour with Unfolds
modern interface, providing consistent UI elements across:
    - django-allauth authentication and social models
    - django-celery-beat periodic task scheduling
    - Djangos built-in User and Group management
    - Token authentication and MFA (multi-factor authentication)

All forms are automatically styled for Unfold, ensuring cohesive design and
responsive layouts across the admin dashboard.
"""

import contextlib

# --- Authentication and Social integrations ---
from allauth.account.decorators import secure_admin_login
from allauth.account.models import EmailAddress
from allauth.mfa.models import Authenticator
from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.models import SocialToken

# --- Core Django modules ---
from django import forms
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.db import models
from django.forms import CheckboxInput
from django.utils.translation import gettext_lazy as _
from django_celery_beat.admin import ClockedScheduleAdmin as BaseClockedScheduleAdmin
from django_celery_beat.admin import CrontabScheduleAdmin as BaseCrontabScheduleAdmin
from django_celery_beat.admin import PeriodicTaskAdmin as BasePeriodicTaskAdmin
from django_celery_beat.admin import PeriodicTaskForm
from django_celery_beat.admin import TaskSelectWidget

# --- Celery periodic task system ---
from django_celery_beat.models import ClockedSchedule
from django_celery_beat.models import CrontabSchedule
from django_celery_beat.models import IntervalSchedule
from django_celery_beat.models import PeriodicTask
from django_celery_beat.models import SolarSchedule

# --- REST Framework and Tokens ---
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.models import TokenProxy

# --- Unfold styling system ---
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.forms import AdminPasswordChangeForm
from unfold.forms import UserChangeForm
from unfold.forms import UserCreationForm
from unfold.widgets import UnfoldAdminSelectWidget
from unfold.widgets import UnfoldAdminTextInputWidget

from .models import User

# ---------------------------------------------------------------------
# Enforce secure login through django-allauth
# ---------------------------------------------------------------------
if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    admin.autodiscover()
    # Wrap the default Django admin login with Allauths MFA-secure version.
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


# ---------------------------------------------------------------------
# Unregister default admin models to re-register with Unfold styling
# ---------------------------------------------------------------------
for model in [
    SocialApp,
    SocialAccount,
    SocialToken,
    EmailAddress,
    Token,
    TokenProxy,
    Group,
    ClockedSchedule,
    CrontabSchedule,
    IntervalSchedule,
    PeriodicTask,
    SolarSchedule,
    Site,
    User,
    Authenticator,
]:
    # Suppresses exceptions if a model is not registered in admin.
    with contextlib.suppress(admin.sites.NotRegistered):
        admin.site.unregister(model)


# ---------------------------------------------------------------------
# Generic Unfold-styled base admin form
# ---------------------------------------------------------------------
class UnfoldStyledAdminForm(forms.ModelForm):
    """
    Provides a base form that automatically applies Unfold-compatible CSS
    classes and layout styling to all admin widgets.

    This ensures visual consistency across third-party and custom admin forms
    without requiring per-field widget overrides.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            widget = field.widget

            # --- Boolean toggle styling (checkbox → toggle switch) ---
            if isinstance(widget, CheckboxInput):
                widget.attrs.update(
                    {
                        "class": "toggle toggle-success",
                        "style": "width:3rem;height:1.5rem;",
                    }
                )
                continue

            # --- Apply Unfolds default input styling ---
            widget.attrs["class"] = (
                f"{widget.attrs.get('class', '')} input input-bordered w-full".strip()
            )

            # Multi-line text boxes styled with consistent row height
            if isinstance(widget, forms.Textarea):
                widget.attrs["rows"] = 6

            # --- Split date/time widget (two separate inputs) ---
            if isinstance(widget, forms.SplitDateTimeWidget):
                # Override with stylised date and time sub-widgets
                field.widget = forms.SplitDateTimeWidget(
                    date_attrs={
                        "type": "date",
                        "class": "input input-bordered",
                        "style": (
                            "width:10rem;height:2.5rem;padding:0.5rem;"
                            "border-radius:0.5rem;"
                        ),
                    },
                    time_attrs={
                        "type": "time",
                        "class": "input input-bordered",
                        "style": (
                            "width:8rem;height:2.5rem;padding:0.5rem;"
                            "border-radius:0.5rem;"
                        ),
                    },
                )
                continue

            # --- HTML5 input type enforcement ---
            if isinstance(widget, forms.DateInput):
                widget.attrs.update({"type": "date"})
            elif isinstance(widget, forms.TimeInput):
                widget.attrs.update({"type": "time"})
            elif isinstance(widget, forms.DateTimeInput):
                widget.attrs.update({"type": "datetime-local"})

            # --- Default inline style baseline for all other widgets ---
            widget.attrs.setdefault(
                "style", "height:2.5rem;padding:0.5rem;border-radius:0.5rem;"
            )


# ---------------------------------------------------------------------
# User Administration
# ---------------------------------------------------------------------
@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    """
    Custom Unfold-compatible admin for the applications custom User model.

    Combines Unfolds styling with Djangos built-in user management features.
    Integrates password management, permission control, and field grouping.
    """

    # Forms defining creation, change, and password reset behaviour
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    # --- Unfold admin behaviour settings ---
    compressed_fields = True  # Compact field layout
    warn_unsaved_form = True  # Unsaved change warnings
    list_filter_sheet = True  # Slide-out filter panel
    list_fullwidth = True  # Full-width list view
    change_form_show_cancel_button = True  # Adds cancel button to forms

    # Apply Unfolds rich-text editor globally to all text fields
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    # --- Django UserAdmin configuration ---
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {"fields": ("name",)}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["email", "name", "is_superuser"]
    search_fields = ["name"]
    ordering = ["id"]
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )


# ---------------------------------------------------------------------
# django-celery-beat integration
# ---------------------------------------------------------------------
class UnfoldTaskSelectWidget(UnfoldAdminSelectWidget, TaskSelectWidget):
    """
    Unfold-styled version of django-celery-beats TaskSelectWidget.

    Combines Unfolds design system with Celerys task selector for periodic
    task creation, ensuring consistency with the rest of the admin interface.
    """


class UnfoldPeriodicTaskForm(PeriodicTaskForm):
    """
    Custom Unfold-compatible form for PeriodicTask entries.

    Overrides the default widget rendering for task and registered task fields
    to use Unfolds visual components for improved readability and usability.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Replace both fields with Unfold-styled widgets
        self.fields["task"].widget = UnfoldAdminTextInputWidget()
        self.fields["regtask"].widget = UnfoldTaskSelectWidget()


# ---------------------------------------------------------------------
# Group and supporting model admin registrations
# ---------------------------------------------------------------------
@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """Unfold-styled admin for Djangos built-in Group model."""

    compressed_fields = True
    warn_unsaved_form = True


# ---------------------------------------------------------------------
# django-allauth and related models
# ---------------------------------------------------------------------
@admin.register(SocialApp)
class SocialAppAdmin(ModelAdmin):
    """Admin for OAuth app registrations (Unfold-styled)."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


@admin.register(SocialAccount)
class SocialAccountAdmin(ModelAdmin):
    """Admin for connected user social accounts (Unfold-styled)."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


@admin.register(SocialToken)
class SocialTokenAdmin(ModelAdmin):
    """Admin for social OAuth tokens (Unfold-styled)."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


@admin.register(EmailAddress)
class EmailAddressAdmin(ModelAdmin):
    """Admin for Allauth email address verification tracking."""

    compressed_fields = True


@admin.register(Token)
class AuthTokenAdmin(ModelAdmin):
    """Admin for DRF authentication tokens (Unfold-styled)."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


@admin.register(Site)
class SiteAdmin(ModelAdmin):
    """Admin for Djangos Site model with Unfold styling."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


@admin.register(Authenticator)
class AuthenticatorAdmin(ModelAdmin):
    """Admin for managing MFA authenticators with Unfold styling."""

    form = UnfoldStyledAdminForm
    compressed_fields = True


# ---------------------------------------------------------------------
# django-celery-beat admin registrations
# ---------------------------------------------------------------------
@admin.register(PeriodicTask)
class PeriodicTaskAdmin(BasePeriodicTaskAdmin, ModelAdmin):
    """Unfold-enhanced admin for managing Celery periodic tasks."""

    form = UnfoldPeriodicTaskForm
    list_fullwidth = True
    warn_unsaved_form = True


@admin.register(IntervalSchedule)
class IntervalScheduleAdmin(ModelAdmin):
    """Unfold-styled admin for Celerys interval schedules."""

    compressed_fields = True


@admin.register(CrontabSchedule)
class CrontabScheduleAdmin(BaseCrontabScheduleAdmin, ModelAdmin):
    """Unfold-styled admin for Celerys crontab schedules."""

    compressed_fields = True


@admin.register(SolarSchedule)
class SolarScheduleAdmin(ModelAdmin):
    """Unfold-styled admin for Celerys solar schedules."""

    compressed_fields = True


@admin.register(ClockedSchedule)
class ClockedScheduleAdmin(BaseClockedScheduleAdmin, ModelAdmin):
    """Unfold-styled admin for Celerys clocked schedules."""

    compressed_fields = True
