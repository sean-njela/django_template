from allauth.account.decorators import secure_admin_login
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin  # (changelog 0.7.0)
from django.contrib.auth.models import Group  # (changelog 0.7.0)
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin  # Unfold base class (changelog 0.7.0)

from .forms import UserAdminChangeForm
from .forms import UserAdminCreationForm
from .models import User

if settings.DJANGO_ADMIN_FORCE_ALLAUTH:
    # Force the `admin` sign in process to go through the `django-allauth` workflow:
    # https://docs.allauth.org/en/latest/common/admin.html#admin
    admin.autodiscover()
    admin.site.login = secure_admin_login(admin.site.login)  # type: ignore[method-assign]


@admin.register(User)
class UserAdmin(
    auth_admin.UserAdmin,
    ModelAdmin,
):  # also inherit from Unfold ModelAdmin (changelog-0.7.0)
    """
    Custom admin configuration for the User model.
    Combines Django's UserAdmin behaviour with Unfold's UI layer.
    """

    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
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
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )


# --- Group Admin Integration (from Unfold docs) ---
# changelog-0.7.0

# Unregister default Django Group admin
admin.site.unregister(Group)


@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    """
    Re-registers Django's Group model with Unfold's ModelAdmin.
    Ensures consistent Unfold styling for group management pages.
    """
