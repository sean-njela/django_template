from django.urls import resolve
from django.urls import reverse
from django.utils.translation import get_language

from django_template.users.models import User


def test_detail(user: User):
    """Ensure user detail URL includes language prefix."""
    lang = get_language() or "en"
    assert (
        reverse("users:detail", kwargs={"pk": user.pk}) == f"/{lang}/users/{user.pk}/"
    )
    assert resolve(f"/{lang}/users/{user.pk}/").view_name == "users:detail"


def test_update():
    """Ensure user update URL includes language prefix."""
    lang = get_language() or "en"
    assert reverse("users:update") == f"/{lang}/users/~update/"
    assert resolve(f"/{lang}/users/~update/").view_name == "users:update"


def test_redirect():
    """Ensure user redirect URL includes language prefix."""
    lang = get_language() or "en"
    assert reverse("users:redirect") == f"/{lang}/users/~redirect/"
    assert resolve(f"/{lang}/users/~redirect/").view_name == "users:redirect"
