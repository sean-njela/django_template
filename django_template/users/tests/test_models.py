from django_template.users.models import User


def test_user_get_absolute_url(user: User):
    """Ensure user absolute URL includes language prefix (i18n_patterns)."""
    assert user.get_absolute_url() == f"/users/{user.pk}/"
