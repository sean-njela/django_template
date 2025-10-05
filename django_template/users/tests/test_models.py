from django.utils.translation import get_language

from django_template.users.models import User


def test_user_get_absolute_url(user: User):
    """Ensure user absolute URL includes language prefix (i18n_patterns)."""
    lang = get_language() or "en"
    assert user.get_absolute_url() == f"/{lang}/users/{user.pk}/"
