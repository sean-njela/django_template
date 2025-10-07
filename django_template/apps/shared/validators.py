from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

ERR_NON_EMPTY = _("Value cannot be empty.")


def validate_non_empty(value: str) -> None:
    if not str(value).strip():
        raise ValidationError(ERR_NON_EMPTY)
