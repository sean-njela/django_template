from django.contrib.auth import get_user_model

User = get_user_model()


def list_users():
    return User.objects.all().only("id", "email", "name").order_by("id")


def get_user(pk: int):
    return User.objects.only("id", "email", "name").get(pk=pk)
