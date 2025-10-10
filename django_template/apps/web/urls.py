from django.urls import path

from .views import index
from .views import people
from .views import user_row_partial

urlpatterns = [
    path("people/", people, name="people"),
    path("cars", index, name="index"),
    path("htmx/user-row/<int:pk>/", user_row_partial, name="user_row_partial"),
]
