from django.contrib.auth import get_user_model
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_GET

from django_template.apps.shared.services import list_users

User = get_user_model()


@require_GET
def people(request: HttpRequest) -> HttpResponse:
    users = list_users()
    return render(request, "web/user_list.html", {"users": users})


@require_GET
def user_row_partial(request: HttpRequest, pk: int) -> HttpResponse:
    u = get_object_or_404(User, pk=pk)
    return render(request, "htmx_partials/user_row.html", {"u": u})
