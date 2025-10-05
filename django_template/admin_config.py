"""Custom Unfold admin callbacks and configuration logic."""
# changelog-0.7.0


def dashboard_callback(request, context):
    """
    Adds custom variables to Unfold dashboard template.
    """
    context.update({"project": "Django Template"})
    return context


def environment_callback(request):
    """
    Returns environment name and label colour for Unfold top-bar badge.
    """
    return ["Production", "success"]


def environment_title_prefix_callback(request):
    """
    Returns a prefix for the <title> tag showing environment name.
    """
    return "[Production] "


def badge_callback(request):
    """
    Example sidebar badge callback.
    """
    return 3 if request.user.is_superuser else None


def permission_callback(request):
    """
    Example sidebar permission check.
    """
    return request.user.is_authenticated and request.user.is_staff
