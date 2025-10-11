"""Comprehensive Unfold demonstration model definitions.

This module defines demonstration models used to illustrate the full range of
Unfolds form and admin UI capabilities. It covers text inputs, numeric types,
date and time fields, file uploads, PostgreSQL-specific array and JSON fields,
and map-based location selection via django-location-field.
"""

from auditlog.registry import auditlog
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.translation import gettext_lazy as _
from location_field.models.plain import PlainLocationField


class DemoCategory(models.Model):
    """
    Represents a simple category entity.

    This model exists solely to demonstrate Unfolds handling of ForeignKey
    relationships in both forms and admin interfaces.

    Fields:
        name (CharField): Category name (required).
        description (TextField): Optional free-text description.

    Meta options:
        verbose_name: Human-readable singular name.
        verbose_name_plural: Human-readable plural name.
    """

    name = models.CharField(_("Name"), max_length=100)
    description = models.TextField(_("Description"), blank=True)

    class Meta:
        verbose_name = _("Demo Category")
        verbose_name_plural = _("Demo Categories")

    def __str__(self):
        """Return the category name for admin display and string conversions."""
        return self.name


class UnfoldDemoModel(models.Model):
    """
    Model designed to demonstrate the complete feature set of Unfolds admin UI.

    Includes a comprehensive range of field types such as:
        - Basic text inputs
        - WYSIWYG editors
        - Choice and boolean toggles
        - Numeric and date/time fields
        - File uploads
        - PostgreSQL ArrayField and JSONField integration
        - Foreign key dropdowns
        - django-location-field for geospatial input via maps

    Each field has a descriptive verbose name and translation-ready labels.
    """

    # ---------------------------------------------------------------------
    # Basic text inputs
    # ---------------------------------------------------------------------
    title = models.CharField(
        _("Title"),
        max_length=200,
        help_text=_("Primary title of the record, displayed in admin listings."),
    )
    subtitle = models.CharField(
        _("Subtitle"),
        max_length=200,
        blank=True,
        help_text=_("Optional subtitle providing additional context."),
    )

    # ---------------------------------------------------------------------
    # Rich text / WYSIWYG
    # ---------------------------------------------------------------------
    content = models.TextField(
        _("Content"),
        blank=True,
        help_text=_(
            "Main body text supporting formatting through Unfolds WYSIWYG editor."
        ),
    )

    # ---------------------------------------------------------------------
    # Choice field (dropdown)
    # ---------------------------------------------------------------------
    STATUS_CHOICES = [
        ("draft", _("Draft")),
        ("review", _("In Review")),
        ("published", _("Published")),
    ]
    status = models.CharField(
        _("Status"),
        max_length=20,
        choices=STATUS_CHOICES,
        default="draft",
        help_text=_("Publication status of this record."),
    )

    # ---------------------------------------------------------------------
    # Boolean toggle
    # ---------------------------------------------------------------------
    is_active = models.BooleanField(
        _("Active"),
        default=True,
        help_text=_("Indicates whether this record is currently active."),
    )

    # ---------------------------------------------------------------------
    # Numeric and date/time fields
    # ---------------------------------------------------------------------
    rating = models.DecimalField(
        _("Rating"),
        max_digits=4,
        decimal_places=2,
        default=0.0,
        help_text=_("Optional decimal rating for evaluation purposes."),
    )
    published_on = models.DateField(
        _("Publish Date"),
        null=True,
        blank=True,
        help_text=_("Date on which the record was or will be published."),
    )
    publish_time = models.TimeField(
        _("Publish Time"),
        null=True,
        blank=True,
        help_text=_("Time of day when the record becomes active."),
    )
    last_reviewed_at = models.DateTimeField(
        _("Last Reviewed"),
        null=True,
        blank=True,
        help_text=_("Timestamp of the last review of this record."),
    )

    # ---------------------------------------------------------------------
    # File upload
    # ---------------------------------------------------------------------
    attachment = models.FileField(
        _("Attachment"),
        upload_to="uploads/demo/",
        blank=True,
        help_text=_("Optional file attachment stored under uploads/demo/."),
    )

    # ---------------------------------------------------------------------
    # Array field (PostgreSQL only)
    # ---------------------------------------------------------------------
    tags = ArrayField(
        base_field=models.CharField(max_length=50),
        verbose_name=_("Tags"),
        blank=True,
        default=list,
        help_text=_("List of keyword tags (requires PostgreSQL backend)."),
    )

    # ---------------------------------------------------------------------
    # JSON field
    # ---------------------------------------------------------------------
    metadata = models.JSONField(
        _("Metadata"),
        blank=True,
        default=dict,
        help_text=_("Optional JSON metadata for storing arbitrary structured data."),
    )

    # ---------------------------------------------------------------------
    # Foreign key relation
    # ---------------------------------------------------------------------
    category = models.ForeignKey(
        DemoCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Category"),
        help_text=_("Associated category selected from DemoCategory."),
    )

    # ---------------------------------------------------------------------
    # Location fields (django-location-field)
    # ---------------------------------------------------------------------
    address = models.CharField(
        _("Address"),
        max_length=255,
        blank=True,
        help_text=_("Address text used as reference for map location."),
    )
    location = PlainLocationField(
        based_fields=["address"],
        zoom=7,
        verbose_name=_("Location"),
        help_text=_("Interactive map field linked to the address input."),
    )

    # ---------------------------------------------------------------------
    # Model metadata
    # ---------------------------------------------------------------------
    class Meta:
        verbose_name = _("Unfold Demo Model")
        verbose_name_plural = _("Unfold Demo Models")
        ordering = ["title"]  # Default ordering alphabetically by title.

    def __str__(self):
        """Return the title for admin list display and string conversions."""
        return self.title


auditlog.register(
    UnfoldDemoModel,
    exclude_fields=["published_on", "publish_time", "last_reviewed_at"],
    mapping_fields={"title": "Name"},
    mask_fields=["address", "location"],
)
auditlog.register(DemoCategory)
