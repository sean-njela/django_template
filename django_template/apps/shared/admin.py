"""Unfold admin integrating django-import-export and location field widgets.

This module demonstrates a comprehensive Unfold admin integration that:
- Uses Unfolds modern widget system for better UX in the Django admin.
- Integrates django-import-export for data import/export capabilities.
- Demonstrates configuration of tabs, filters, and fieldsets.
- Automatically styles all forms through Unfolds form and widget overrides.
"""

from django import forms
from django.contrib import admin
from django.db import models
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.forms.widgets import ArrayWidget
from unfold.contrib.forms.widgets import WysiwygWidget
from unfold.contrib.import_export.forms import ExportForm
from unfold.contrib.import_export.forms import ImportForm
from unfold.widgets import UnfoldAdminSelectWidget
from unfold.widgets import UnfoldAdminTextInputWidget

from django_template.apps.shared.models.cars.models import Car
from django_template.apps.shared.models.demo.models import DemoCategory
from django_template.apps.shared.models.demo.models import UnfoldDemoModel


# ---------------------------------------------------------------------
# django-import-export Resource
# ---------------------------------------------------------------------
class UnfoldDemoResource(resources.ModelResource):
    """
    Defines how `UnfoldDemoModel` data is imported and exported.

    This resource class controls which fields are serialised and in what order.
    It ensures that unchanged records are skipped and that model instances are
    cleaned before saving.

    Attributes:
        model: Target model for import/export operations.
        skip_unchanged: Whether unchanged rows are ignored.
        report_skipped: Whether skipped rows are shown in reports.
        clean_model_instances: Whether to run model cleaning before saving.
        fields: Explicit list of fields to include in export/import.
        export_order: Defines column order in exported datasets.
    """

    class Meta:
        model = UnfoldDemoModel
        skip_unchanged = True
        report_skipped = True
        clean_model_instances = True
        fields = (
            "id",
            "title",
            "subtitle",
            "status",
            "is_active",
            "rating",
            "published_on",
            "publish_time",
            "last_reviewed_at",
            "tags",
            "metadata",
            "category__name",
            "address",
            "location",
        )
        export_order = fields


# ---------------------------------------------------------------------
# Custom Unfold Form
# ---------------------------------------------------------------------
class UnfoldDemoForm(forms.ModelForm):
    """
    Form definition for `UnfoldDemoModel` using Unfolds custom widgets.

    This form demonstrates Unfolds widget system integration for multiple field
    types, including text inputs, selects, array fields, and rich text editors.

    The location field is automatically handled by django-location-fields
    internal widgets and does not require manual widget assignment.
    """

    class Meta:
        model = UnfoldDemoModel
        fields = [
            "title",
            "subtitle",
            "content",
            "status",
            "is_active",
            "rating",
            "published_on",
            "publish_time",
            "last_reviewed_at",
            "attachment",
            "tags",
            "metadata",
            "category",
            "address",
            "location",
        ]
        widgets = {
            # Use Unfold-styled text input widgets for short text fields
            "title": UnfoldAdminTextInputWidget,
            "subtitle": UnfoldAdminTextInputWidget,
            # Use styled select widgets for dropdown fields
            "status": UnfoldAdminSelectWidget,
            "category": UnfoldAdminSelectWidget,
            # PostgreSQL ArrayField with Unfolds array widget
            "tags": ArrayWidget,
            # Unfold WYSIWYG editor for formatted text content
            "content": WysiwygWidget,
        }


# ---------------------------------------------------------------------
# Unfold Admin Registrations + ImportExport Admin
# ---------------------------------------------------------------------
@admin.register(UnfoldDemoModel)
class UnfoldDemoAdmin(ModelAdmin, ImportExportModelAdmin):
    """
    Comprehensive Unfold admin integration for UnfoldDemoModel.

    This class combines Unfolds visual enhancements with django-import-exports
    data import/export features. It demonstrates:
      - Advanced Unfold list and form configurations.
      - Custom import/export form integration for consistent styling.
      - Use of field tabs for logical form organisation.
      - Safe overrides for text fields and visual form behaviour.
    """

    # --- django-import-export integration ---
    # Resource defines which fields to include and how theyre processed.
    resource_class = UnfoldDemoResource

    # Unfolds themed import/export form classes ensure UI consistency.
    import_form_class = ImportForm
    export_form_class = ExportForm

    # Use the Unfold-styled form defined above.
    form = UnfoldDemoForm

    # --- Django admin configuration ---
    list_display = (
        "title",
        "status",
        "is_active",
        "rating",
        "published_on",
        "category",
    )
    list_filter = ("status", "is_active", "category")
    search_fields = ("title", "subtitle", "tags")
    ordering = ("title",)

    # --- Unfold-specific configuration ---
    # These improve UI and user experience in the admin interface.
    compressed_fields = True  # Collapses form fields for compact display.
    warn_unsaved_form = True  # Prompts users before leaving unsaved forms.
    list_fullwidth = True  # Uses full viewport width for changelist table.
    list_filter_sheet = True  # Displays filters in slide-over sidebar.
    change_form_show_cancel_button = True  # Adds cancel button to forms.

    # Apply Unfolds WYSIWYG editor to all TextField instances globally.
    formfield_overrides = {
        models.TextField: {"widget": WysiwygWidget},
    }

    # --- Unfold tabs configuration ---
    # Groups related fields logically into sections for clarity.
    tabs = {
        "General": {
            "fields": (
                "title",
                "subtitle",
                "status",
                "is_active",
                "category",
            )
        },
        "Content": {"fields": ("content", "tags", "metadata", "attachment")},
        "Publishing": {
            "fields": (
                "rating",
                "published_on",
                "publish_time",
                "last_reviewed_at",
            )
        },
        "Location": {"fields": ("address", "location")},
    }


@admin.register(Car)
class CarAdmin(ModelAdmin):
    """
    Basic Unfold admin interface for the Car model.

    Provides a minimal interface demonstrating how Unfold automatically
    enhances even simple models with clean layout and consistent styling.
    """


@admin.register(DemoCategory)
class DemoCategoryAdmin(ModelAdmin):
    """
    Basic Unfold admin interface for the DemoCategory model.

    Provides a minimal interface demonstrating how Unfold automatically
    enhances even simple models with clean layout and consistent styling.
    """

    list_display = ("name", "description")
    search_fields = ("name",)
    compressed_fields = True  # Collapses form sections for concise layout.
