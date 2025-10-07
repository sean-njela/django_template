from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PublicUserViewSet

router = DefaultRouter()
router.register(r"public-users", PublicUserViewSet, basename="public-user")

urlpatterns = [path("", include(router.urls))]
