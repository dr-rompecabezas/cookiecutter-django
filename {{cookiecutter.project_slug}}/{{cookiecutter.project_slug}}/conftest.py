import pytest

from {{ cookiecutter.project_slug }}.apps.users.models import User
from {{ cookiecutter.project_slug }}.apps.users.tests.factories import UserFactory


@pytest.fixture(autouse=True)
def media_storage(settings, tmpdir):
    settings.MEDIA_ROOT = tmpdir.strpath


@pytest.fixture
def user(db) -> User:
    return UserFactory()


@pytest.fixture()
def admin_user(
    db: None,
    django_user_model,
    django_username_field: str,
) -> User:
    """A Django admin user.

    This uses an existing user with username "admin", or creates a new one with
    password "password".
    """
    UserModel = django_user_model
    username_field = django_username_field
    username = "admin@example.com" if username_field == "email" else "admin"

    try:
        user = UserModel._default_manager.get_by_natural_key(username)
    except UserModel.DoesNotExist:
        user_data = {}
        if "email" in UserModel.REQUIRED_FIELDS:
            user_data["email"] = "admin@example.com"
        user_data["password"] = "password"
        user_data[username_field] = username
        user_data["first_name"] = "Admin"
        user_data["last_name"] = "User"
        user = UserModel._default_manager.create_superuser(**user_data)
    return user
