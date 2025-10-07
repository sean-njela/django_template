from rest_framework import permissions
from rest_framework import viewsets

from django_template.apps.shared.services import list_users

from .serializers import PublicUserSerializer

# Create your views here.


class PublicUserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PublicUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return list_users()
