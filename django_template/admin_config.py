"""Custom Unfold admin configuration and callbacks.

This module defines all runtime callbacks used by Unfold to dynamically
customise the Django admin interface. It supports environment-aware
badges, context-driven dashboard data, and dynamic sidebar permissions.

All functions here are loaded lazily by Unfold through dotted-path
imports defined in the UNFOLD settings dictionary. This ensures that
the admin environment remains responsive and dynamically reflects the
current environment and request context.
"""

import os

from django.contrib.auth.models import AnonymousUser


def dashboard_callback(request, context):
    """
    Extend the Unfold dashboard context with project and environment data.

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request.
    context : dict
        The default Unfold dashboard context.

    Returns
    -------
    dict
        The updated context containing additional variables for the template.
    """
    environment = os.getenv("DJANGO_ENV", "development").capitalize()
    context.update(
        {
            "project": "Django Template",
            "environment": environment,
        }
    )
    return context


def environment_callback(request):
    """
    Return a two-element list used by Unfold to render the environment badge.

    The first element is the environment label, and the second is the
    Tailwind-compatible colour key for badge styling. This is dynamically
    computed from the DJANGO_ENV environment variable.

    Examples
    --------
    ["Development", "warning"]
    ["Staging", "info"]
    ["Production", "success"]

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request.

    Returns
    -------
    list[str, str]
        The environment label and badge colour.
    """
    env = os.getenv("DJANGO_ENV", "development").capitalize()
    colour_map = {
        "Development": "warning",
        "Local": "info",
        "Staging": "info",
        "Production": "success",
    }
    colour = colour_map.get(env, "neutral")
    return [env, colour]


def environment_title_prefix_callback(request):
    """
    Return a prefix string for the <title> tag in the admin interface.

    This helps clearly identify which environment the admin interface
    is connected to (for example, when running multiple environments
    such as staging and production simultaneously).

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request.

    Returns
    -------
    str
        A string prefix such as "[Production] ".
    """
    env = os.getenv("DJANGO_ENV", "development").capitalize()
    return f"[{env}] "


def badge_callback(request):
    """
    Example sidebar badge callback.

    Returns a numeric badge count visible in the Unfold sidebar next to
    the linked item. Can be replaced with dynamic logic such as pending
    approvals or unread messages.

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request.

    Returns
    -------
    int | None
        Integer count for badge display, or None for no badge.
    """
    if isinstance(request.user, AnonymousUser):
        return None
    return 3 if request.user.is_superuser else None


def permission_callback(request):
    """
    Example sidebar permission check callback.

    Determines whether a given navigation item should be visible in the
    sidebar based on user permissions.

    Parameters
    ----------
    request : HttpRequest
        The current HTTP request.

    Returns
    -------
    bool
        True if the item should be visible, False otherwise.
    """
    user = request.user
    return bool(user.is_authenticated and user.is_staff)
